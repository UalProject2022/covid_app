from datetime import datetime

import pandas as pd
from covid_site.etl.tools import ETLProcessStatus, run_etl
from covid_site.models import County, TotalDeaths
from django.db import transaction

NEW_COLUMN_NAMES = {
    'Concelho': 'county',
}

RIGHT_COUNTY_NAME = {
    'Calheta (R.A.A.)': 'CALHETA (AÇORES)',
    'Calheta (R.A.M.)': 'CALHETA',
    'Lagoa': 'LAGOA (FARO)',
    'Lagoa (R.A.A)': 'LAGOA',
}

IGNORE_COUNTIES = [
    'Desconhecido',
    'Estrangeiro',
]


def dados_sico_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the files that match the pattern
        Dados_SICO_XXX.csv.

    Args:
        df (pd.DataFrame): the DataFrame loaded from the CSV file.

    Returns:
        ETLProcessStatus: the status of the ETL process, containing the error
            (if any).
    '''

    try:
        df.rename(columns=NEW_COLUMN_NAMES, inplace=True)

        run_etl(
            df=df,
            django_model=TotalDeaths,
            specific_etl_method=generate_total_deaths_records,
        )

        status = ETLProcessStatus(
            succeeded=True,
            message='Tables updated with success.',
        )

    except Exception as e:
        print(e)
        status = ETLProcessStatus(
            succeeded=False,
            message='Error during update process, please check the provided file.',
            exception=e,
        )

    return status


def extract_week_date(date: str, day: int) -> datetime:
    '''Extracts the date object from a specific week of a year.

    Args:
        date (str): the string date from which to extract the date object.
        day (int): the day of the week to use.

    Returns:
        datetime: the date object extracted.
    '''

    return datetime.strptime(date + f'-{day}', 'Semana %V-%G-%u')


@transaction.atomic
def generate_total_deaths_records(df: pd.DataFrame) -> list[TotalDeaths]:
    '''Generates records for the Total Deaths table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[TotalDeaths]: list of objects to be inserted / updated.
    '''

    counties = County.objects.all()

    # Remove the "county" column
    weeks = list(df.columns)[1:]

    main_year = extract_week_date(date=weeks[0], day=1).year
    if main_year != extract_week_date(date=weeks[0], day=7):
        main_year += 1

    records = list()
    for row in df.to_dict(orient='records'):

        county_name = row['county']

        if county_name in IGNORE_COUNTIES:
            continue

        if county_name in RIGHT_COUNTY_NAME:
            county_name = RIGHT_COUNTY_NAME[county_name]

        county = counties.filter(county_name=county_name).first()

        for week in weeks:

            date_start = extract_week_date(date=week, day=1)
            date_end = extract_week_date(date=week, day=7)

            if week == weeks[0]:
                day = 1
                while date_start.year != main_year:
                    day += 1
                    date_start = extract_week_date(date=week, day=day)
            elif week == weeks[-1]:
                day = 7
                while date_end.year != main_year:
                    day -= 1
                    date_end = extract_week_date(date=week, day=day)

            obj = TotalDeaths(
                county=county,
                date_start=date_start,
                date_end=date_end,
                deaths=row[week],
            )

            records.append(obj)

    return records

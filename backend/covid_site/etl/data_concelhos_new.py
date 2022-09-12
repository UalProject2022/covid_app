from collections import defaultdict

import pandas as pd
from covid_site.etl.data import generate_age_records
from covid_site.etl.tools import ETLProcessStatus, run_etl
from covid_site.models import (Age, County, Incidence, IncidenceCategory,
                               PopulationByAge, Region)
from django.db import transaction

NEW_COLUMN_NAMES = {
    'data': 'reference_date',
    'concelho': 'county_name',
    'confirmados_14': 'confirmed_14',
    'confirmados_1': 'confirmed_1',
    'incidencia': 'incidence',
    'incidencia_categoria': 'incidence_category',
    'incidencia_risco': 'incidence_risk',

    'tendencia_incidencia': 'tendency_incidence',
    'tendencia_categoria': 'tendency_category',
    'tendencia_desc': 'tendency_description',

    'casos_14dias': 'cases_14',
    'ars': 'ars',
    'distrito': 'district',
    'dicofre': 'dicofre',
    'area': 'area',
    'population': 'population',
    'population_65_69': 'population_65_69',
    'population_70_74': 'population_70_74',
    'population_75_79': 'population_75_79',
    'population_80_84': 'population_80_84',
    'population_85_mais': 'population_85_plus',
    'population_80_mais': 'population_80_plus',
    'population_75_mais': 'population_75_plus',
    'population_70_mais': 'population_70_plus',
    'population_65_mais': 'population_65_plus',
    'densidade_populacional': 'population_density',
    'densidade_1': 'density_1',
    'densidade_2': 'density_2',
    'densidade_3': 'density_3',
}


def data_concelhos_new_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the data_concelhos_new.csv file.

    Args:
        df (pd.DataFrame): the DataFrame loaded from the CSV file.

    Returns:
        ETLProcessStatus: the status of the ETL process, containing the error
            (if any).
    '''

    try:
        df.rename(columns=NEW_COLUMN_NAMES, inplace=True)
        df['ars'] = df['ars'].apply(get_ars_english_value)

        df['reference_date'] = pd.to_datetime(
            df['reference_date'],
            format=f'%d-%m-%Y',
            utc=True,
        )

        run_etl(
            df=df,
            django_model=County,
            specific_etl_method=generate_county_records,
        )

        run_etl(
            df=df,
            django_model=Age,
            specific_etl_method=generate_age_records,
        )

        run_etl(
            df=df,
            django_model=PopulationByAge,
            specific_etl_method=generate_population_by_age_records,
            delete_if_all_none=('people',),
        )

        run_etl(
            df=df,
            django_model=Incidence,
            specific_etl_method=generate_incidence_records,
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


def get_ars_english_value(ars: str) -> str:
    '''Converts the ARS value in Portuguese to English.

    Args:
        ars (str): the ARS in Portuguese.

    Returns:
        str: the ARS in English.
    '''

    if ars == 'Centro':
        return 'Center'
    elif ars == 'Norte':
        return 'North'
    elif ars == 'Sul':
        return 'South'
    else:
        return ars


@transaction.atomic
def generate_county_records(df: pd.DataFrame) -> list[County]:
    '''Generates records for the County table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[County]: list of objects to be inserted / updated.
    '''

    regions = Region.objects.all()

    records = dict()
    for row in df.to_dict(orient='records'):

        if row['dicofre'] not in records.keys():

            obj = County(
                dicofre=row['dicofre'],
                district=row['district'],
                county_name=row['county_name'],
                region=regions.filter(name=row['ars']).first(),
                area=row['area'],
                population=row['population'],
                population_density=row['population_density'],
                density_1=row['density_1'],
                density_2=row['density_2'],
                density_3=row['density_3'],
            )

            records[obj.dicofre] = obj
        else:
            obj = records[row['dicofre']]
            obj.area = row['area']
            obj.population = row['population']
            obj.population_density = row['population_density']
            obj.density_1 = row['density_1']
            obj.density_2 = row['density_2']
            obj.density_3 = row['density_3']

            records[obj.dicofre] = obj

    return list(records.values())


@transaction.atomic
def generate_population_by_age_records(df: pd.DataFrame) -> list[PopulationByAge]:
    '''Generates records for the Population By Age table according to the
        provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[PopulationByAge]: list of objects to be inserted / updated.
    '''

    records = defaultdict(dict)
    counties = County.objects.all()
    age_ranges = Age.objects.all()

    ages = [
        ('65', '69'),
        ('70', '74'),
        ('75', '79'),
        ('80', '84'),
        ('65', None),
        ('70', None),
        ('75', None),
        ('80', None),
        ('85', None),
    ]

    ages = [age_ranges.filter(
        age_start=age[0], age_end=age[1]).first() for age in ages]

    for row in df.to_dict(orient='records'):

        for age in ages:
            range_end = age.age_end if age.age_end is not None else 'plus'
            col_filter = f'{age.age_start}_{range_end}'

            if row['dicofre'] not in records[col_filter].keys():

                obj = PopulationByAge(
                    age=age,
                    county=counties.filter(dicofre=row['dicofre']).first(),
                    people=row[f'population_{col_filter}'],
                )

                records[col_filter][row['dicofre']] = obj
            else:
                obj = records[col_filter][row['dicofre']]
                obj.people = row[f'population_{col_filter}']

                records[col_filter][row['dicofre']] = obj

    filtered_records = list()
    for _, records in records.items():
        filtered_records.extend(list(records.values()))

    return filtered_records


@transaction.atomic
def generate_incidence_records(df: pd.DataFrame) -> list[Incidence]:
    '''Generates records for the Incidence table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Incidence]: list of objects to be inserted / updated.
    '''

    counties = County.objects.all()
    categories = IncidenceCategory.objects.all()

    records = list()
    for row in df.to_dict(orient='records'):

        category = categories.filter(
            category_lower_limit__lte=row['incidence'],
        ).order_by('-category_lower_limit').first()

        obj = Incidence(
            reference_date=row['reference_date'],
            county=counties.filter(dicofre=row['dicofre']).first(),
            incidence_category=category,
            incidence=row['incidence'],
            cases_14=row['cases_14'],
            confirmed_1=row['confirmed_1'],
            confirmed_14=row['confirmed_14'],
        )

        records.append(obj)

    return records

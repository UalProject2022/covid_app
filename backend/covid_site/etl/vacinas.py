import pandas as pd
from covid_site.etl.data import generate_age_records
from covid_site.etl.tools import ETLProcessStatus, get_table_cols, run_etl
from covid_site.models import Age, Reinforcement, Vaccines
from django.db import transaction

NEW_COLUMN_NAMES = {
    'data': 'reference_date',
    'doses': 'doses',
    'doses_novas': 'doses_new',
    'doses1': 'doses_1',
    'doses1_novas': 'doses_1_new',
    'doses2': 'doses_2',
    'doses2_novas': 'doses_2_new',
    'pessoas_vacinadas_completamente': 'vaccinated_fully',
    'pessoas_vacinadas_completamente_novas': 'vaccinated_fully_new',
    'pessoas_vacinadas_parcialmente': 'vaccinated_partially',
    'pessoas_vacinadas_parcialmente_novas': 'vaccinated_partially_new',
    'pessoas_inoculadas': 'inoculated',
    'pessoas_inoculadas_novas': 'inoculated_new',
    'pessoas_inoculadas_12mais': 'inoculated_12_plus',
    'vacinas': 'vaccines',
    'vacinas_novas': 'vaccines_new',
    'pessoas_vacinadas_completamente_continente': 'vaccinated_fully_continent',
    'pessoas_vacinadas_completamente_continente_novas': 'vaccinated_fully_continent_new',
    'pessoas_reforço': 'reinforcement',
    'pessoas_reforço_novas': 'reinforce_new',
    'pessoas_reforço_continente': 'reinforcement_continent',
    'pessoas_reforço_continente_novas': 'reinforcement_continent_new',
    'pessoas_gripe': 'flu',
    'pessoas_gripe_novas': 'flu_new',
    'vacinas_reforço_e_gripe_novas': 'reinforcement_and_flu_new',
    'reforço_80mais': 'reinforcement_80_plus',
    'reforço_80mais_novas': 'reinforcement_80_plus_new',
    'reforço_70_79': 'reinforcement_70_79',
    'reforço_70_79_novas': 'reinforcement_70_79_new',
    'reforço_65_69': 'reinforcement_65_69',
    'reforço_65_69_novas': 'reinforcement_65_69_new',
    'reforço_60_69': 'reinforcement_60_69',
    'reforço_60_69_novas': 'reinforcement_60_69_new',
    'reforço_50_59': 'reinforcement_50_59',
    'reforço_50_59_novas': 'reinforcement_50_59_new',
    'reforço_40_49': 'reinforcement_40_49',
    'reforço_40_49_novas': 'reinforcement_40_49_new',
    'reforço_30_39': 'reinforcement_30_39',
    'reforço_30_39_novas': 'reinforcement_30_39_new',
    'reforço_18_29': 'reinforcement_18_29',
    'reforço_18_29_novas': 'reinforcement_18_29_new',
    'vacinação_iniciada_05_11': 'vaccination_started_05_11',
    'vacinação_iniciada_05_11_novas': 'vaccination_started_05_11_new',
    'vacinação_completa_05_11': 'vaccination_complete_05_11',
    'vacinação_completa_05_11_novas': 'vaccination_complete_05_11_new',
}


def vacinas_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the vacinas.csv file.

    Args:
        df (pd.DataFrame): the DataFrame loaded from the CSV file.

    Returns:
        ETLProcessStatus: the status of the ETL process, containing the error
            (if any).
    '''

    try:
        df.rename(columns=NEW_COLUMN_NAMES, inplace=True)

        date_columns_formats = {
            'reference_date': f'%d-%m-%Y',
        }

        for c, f in date_columns_formats.items():
            df[c] = pd.to_datetime(df[c], format=f, utc=True)

        run_etl(
            df=df,
            django_model=Vaccines,
            specific_etl_method=generate_vaccines_records,
        )

        run_etl(
            df=df,
            django_model=Age,
            specific_etl_method=generate_age_records,
        )

        run_etl(
            df=df,
            django_model=Reinforcement,
            specific_etl_method=generate_reinforcement_records,
            delete_if_all_none=(
                'total',
                'new',
            ),
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


@transaction.atomic
def generate_vaccines_records(
    df: pd.DataFrame,
) -> list[Vaccines]:
    '''Generates records for the Vaccines table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Vaccines]: list of objects to be inserted / updated.
    '''

    table_columns = get_table_cols(Vaccines)

    records = list()
    for row in df[table_columns].to_dict(orient='records'):
        records.append(Vaccines(**row))

    return records


@transaction.atomic
def generate_reinforcement_records(df: pd.DataFrame) -> list[Reinforcement]:
    '''Generates records for the Reinforcement table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Reinforcement]: list of objects to be inserted / updated.
    '''

    age_ranges = Age.objects.all()

    ages = [
        ('18', '29'),
        ('30', '39'),
        ('40', '49'),
        ('50', '59'),
        ('60', '69'),
        ('65', '69'),
        ('70', '79'),
        ('80', None),
    ]

    ages = [age_ranges.filter(
        age_start=age[0], age_end=age[1]).first() for age in ages]

    records = list()
    for row in df.to_dict(orient='records'):

        for age in ages:
            range_end = age.age_end if age.age_end is not None else 'plus'
            col_filter = f'{age.age_start}_{range_end}'

            obj = Reinforcement(
                reference_date=row['reference_date'],
                total=row[f'reinforcement_{col_filter}'],
                new=row[f'reinforcement_{col_filter}_new'],
                age=age,
            )

            records.append(obj)

    return records

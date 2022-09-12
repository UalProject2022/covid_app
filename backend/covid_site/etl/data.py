import pandas as pd
from covid_site.etl.tools import ETLProcessStatus, get_table_cols, run_etl
from covid_site.models import (Age, GeneralData, Region, StatisticsByAgeAndSex,
                               StatisticsByRegion, StatisticsBySex, Symptoms,
                               SymptomsType)
from django.db import transaction

NEW_COLUMN_NAMES = {
    'data': 'reference_date',
    'data_dados': 'release_date',
    'confirmados': 'confirmed',

    'confirmados_arsnorte': 'confirmed_north',
    'confirmados_arscentro': 'confirmed_center',
    'confirmados_arslvt': 'confirmed_lvt',
    'confirmados_arsalentejo': 'confirmed_alentejo',
    'confirmados_arsalgarve': 'confirmed_algarve',
    'confirmados_acores': 'confirmed_acores',
    'confirmados_madeira': 'confirmed_madeira',
    'confirmados_estrangeiro': 'confirmed_foreign',

    'confirmados_novos': 'confirmed_new',

    'recuperados': 'recovered',
    'obitos': 'deaths',
    'internados': 'interned',
    'internados_uci': 'interned_icu',
    'lab': 'lab',
    'suspeitos': 'suspects',
    'vigilancia': 'vigilance',
    'n_confirmados': 'not_confirmed',
    'cadeias_transmissao': 'transmission_chains',
    'transmissao_importada': 'transmission_imported',

    'confirmados_0_9_f': 'confirmed_0_9_f',
    'confirmados_0_9_m': 'confirmed_0_9_m',
    'confirmados_10_19_f': 'confirmed_10_19_f',
    'confirmados_10_19_m': 'confirmed_10_19_m',
    'confirmados_20_29_f': 'confirmed_20_29_f',
    'confirmados_20_29_m': 'confirmed_20_29_m',
    'confirmados_30_39_f': 'confirmed_30_39_f',
    'confirmados_30_39_m': 'confirmed_30_39_m',
    'confirmados_40_49_f': 'confirmed_40_49_f',
    'confirmados_40_49_m': 'confirmed_40_49_m',
    'confirmados_50_59_f': 'confirmed_50_59_f',
    'confirmados_50_59_m': 'confirmed_50_59_m',
    'confirmados_60_69_f': 'confirmed_60_69_f',
    'confirmados_60_69_m': 'confirmed_60_69_m',
    'confirmados_70_79_f': 'confirmed_70_79_f',
    'confirmados_70_79_m': 'confirmed_70_79_m',
    'confirmados_80_plus_f': 'confirmed_80_plus_f',
    'confirmados_80_plus_m': 'confirmed_80_plus_m',

    'sintomas_tosse': 'symptoms_cough',
    'sintomas_febre': 'symptoms_fever',
    'sintomas_dificuldade_respiratoria': 'symptoms_difficulty_breathing',
    'sintomas_cefaleia': 'symptoms_nausea',
    'sintomas_dores_musculares': 'symptoms_muscle_pain',
    'sintomas_fraqueza_generalizada': 'symptoms_generalized_weakness',

    'confirmados_f': 'confirmed_f',
    'confirmados_m': 'confirmed_m',

    'obitos_arsnorte': 'deaths_north',
    'obitos_arscentro': 'deaths_center',
    'obitos_arslvt': 'deaths_lvt',
    'obitos_arsalentejo': 'deaths_alentejo',
    'obitos_arsalgarve': 'deaths_algarve',
    'obitos_acores': 'deaths_acores',
    'obitos_madeira': 'deaths_madeira',
    'obitos_estrangeiro': 'deaths_foreign',

    'recuperados_arsnorte': 'recovered_north',
    'recuperados_arscentro': 'recovered_center',
    'recuperados_arslvt': 'recovered_lvt',
    'recuperados_arsalentejo': 'recovered_alentejo',
    'recuperados_arsalgarve': 'recovered_algarve',
    'recuperados_acores': 'recovered_acores',
    'recuperados_madeira': 'recovered_madeira',
    'recuperados_estrangeiro': 'recovered_foreign',

    'obitos_0_9_f': 'deaths_0_9_f',
    'obitos_0_9_m': 'deaths_0_9_m',
    'obitos_10_19_f': 'deaths_10_19_f',
    'obitos_10_19_m': 'deaths_10_19_m',
    'obitos_20_29_f': 'deaths_20_29_f',
    'obitos_20_29_m': 'deaths_20_29_m',
    'obitos_30_39_f': 'deaths_30_39_f',
    'obitos_30_39_m': 'deaths_30_39_m',
    'obitos_40_49_f': 'deaths_40_49_f',
    'obitos_40_49_m': 'deaths_40_49_m',
    'obitos_50_59_f': 'deaths_50_59_f',
    'obitos_50_59_m': 'deaths_50_59_m',
    'obitos_60_69_f': 'deaths_60_69_f',
    'obitos_60_69_m': 'deaths_60_69_m',
    'obitos_70_79_f': 'deaths_70_79_f',
    'obitos_70_79_m': 'deaths_70_79_m',
    'obitos_80_plus_f': 'deaths_80_plus_f',
    'obitos_80_plus_m': 'deaths_80_plus_m',

    'obitos_f': 'deaths_f',
    'obitos_m': 'deaths_m',

    'confirmados_desconhecidos_m': 'confirmed_unknown_m',
    'confirmados_desconhecidos_f': 'confirmed_unknown_f',

    'ativos': 'active',

    'internados_enfermaria': 'interned_infirmary',

    'confirmados_desconhecidos': 'confirmed_unknown',

    'incidencia_nacional': 'incidence_national',
    'incidencia_continente': 'incidence_continent',

    'rt_nacional': 'rt_national',
    'rt_continente': 'rt_continent',
}


def data_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the data.csv file.

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
            'release_date': f'%d-%m-%Y %H:%M',
        }

        for c, f in date_columns_formats.items():
            df[c] = pd.to_datetime(df[c], format=f, utc=True)

        run_etl(
            df=df,
            django_model=GeneralData,
            specific_etl_method=generate_general_data_records,
        )

        run_etl(
            df=df,
            django_model=StatisticsBySex,
            specific_etl_method=generate_statistics_by_sex_records,
            delete_if_all_none=(
                'confirmed',
                'confirmed_unknown',
                'deaths',
            ),
        )

        run_etl(
            df=df,
            django_model=Age,
            specific_etl_method=generate_age_records,
        )

        run_etl(
            df=df,
            django_model=StatisticsByAgeAndSex,
            specific_etl_method=generate_statistics_by_age_and_sex_records,
            delete_if_all_none=('confirmed', 'deaths'),
        )

        run_etl(
            df=df,
            django_model=SymptomsType,
            specific_etl_method=generate_symptoms_type_records,
        )

        run_etl(
            df=df,
            django_model=Symptoms,
            specific_etl_method=generate_symptoms_records,
            delete_if_all_none=('quantity',),
        )

        run_etl(
            df=df,
            django_model=StatisticsByRegion,
            specific_etl_method=generate_statistics_by_region_records,
            delete_if_all_none=('confirmed', 'deaths', 'recovered'),
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
def generate_general_data_records(df: pd.DataFrame) -> list[GeneralData]:
    '''Generates records for the General Data table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[GeneralData]: list of objects to be inserted / updated.
    '''

    table_columns = get_table_cols(GeneralData)

    records = list()
    for row in df[table_columns].to_dict(orient='records'):
        records.append(GeneralData(**row))

    return records


@transaction.atomic
def generate_statistics_by_sex_records(df: pd.DataFrame) -> list[StatisticsBySex]:
    '''Generates records for the Statistics by Sex table according to the
        provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[StatisticsBySex]: list of objects to be inserted / updated.
    '''

    records = list()
    for row in df.to_dict(orient='records'):

        for sex in ['m', 'f']:
            obj = StatisticsBySex(
                reference_date=row['reference_date'],
                sex=sex,
                confirmed=row[f'confirmed_{sex}'],
                confirmed_unknown=row[f'confirmed_unknown_{sex}'],
                deaths=row[f'deaths_{sex}'],
            )

            records.append(obj)

    return records


@transaction.atomic
def generate_age_records(df: pd.DataFrame) -> list[Age]:
    '''Generates records for the Age table according to the provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Age]: list of objects to be inserted / updated.
    '''

    list_of_ages = set()
    for c in list(df.columns):
        list_of_numbers = tuple(s for s in c.split(
            '_') if s.isdigit() or s == 'plus')

        if len(list_of_numbers) == 2:
            list_of_ages.add(list_of_numbers)

    records = list()
    for age_range in list_of_ages:
        obj = Age(
            age_start=age_range[0],
            age_end=age_range[1] if age_range[1] != 'plus' else None,
        )

        records.append(obj)

    return records


@transaction.atomic
def generate_statistics_by_age_and_sex_records(df: pd.DataFrame) -> list[StatisticsByAgeAndSex]:
    '''Generates records for the Statistics by Age and Sex table according to
        the provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[StatisticsByAgeAndSex]: list of objects to be inserted / updated.
    '''

    age_ranges = Age.objects.all()

    ages = [
        ('0', '9'),
        ('10', '19'),
        ('20', '29'),
        ('30', '39'),
        ('40', '49'),
        ('50', '59'),
        ('60', '69'),
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

            for sex in ['m', 'f']:
                obj = StatisticsByAgeAndSex(
                    reference_date=row['reference_date'],
                    age=age,
                    sex=sex,
                    confirmed=row[f'confirmed_{col_filter}_{sex}'],
                    deaths=row[f'deaths_{col_filter}_{sex}'],
                )

                records.append(obj)

    return records


@transaction.atomic
def generate_symptoms_type_records(df: pd.DataFrame) -> list[SymptomsType]:
    '''Generates records for the Symptoms Type table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[SymptomsType]: list of objects to be inserted / updated.
    '''

    symptoms_types = set()
    for c in list(df.columns):
        if c.startswith('symptoms_'):
            symptoms_type = ' '.join(c.split('_')[1:])
            symptoms_types.add(symptoms_type)

    records = list()
    for symptoms_type in symptoms_types:
        obj = SymptomsType(
            type=symptoms_type,
        )

        records.append(obj)

    return records


@transaction.atomic
def generate_symptoms_records(df: pd.DataFrame) -> list[Symptoms]:
    '''Generates records for the Symptoms table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Symptoms]: list of objects to be inserted / updated.
    '''

    symptoms_types = SymptomsType.objects.all()

    records = list()
    for row in df.to_dict(orient='records'):

        for symptoms_type in symptoms_types.iterator():
            column = '_'.join(['symptoms'] + symptoms_type.type.split())

            obj = Symptoms(
                reference_date=row['reference_date'],
                symptoms_type=symptoms_type,
                quantity=row[column],
            )

            records.append(obj)

    return records


@transaction.atomic
def generate_statistics_by_region_records(df: pd.DataFrame) -> list[StatisticsByRegion]:
    '''Generates records for the Statistics by Region table according to the
        provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[StatisticsByRegion]: list of objects to be inserted / updated.
    '''

    regions = Region.objects.exclude(short_name__in=['national', 'continent'])

    records = list()
    for row in df.to_dict(orient='records'):

        for region in regions.iterator():
            region_short_name = region.short_name

            obj = StatisticsByRegion(
                reference_date=row['reference_date'],
                region=region,
                confirmed=row[f'confirmed_{region_short_name}'],
                deaths=row[f'deaths_{region_short_name}'],
                recovered=row[f'recovered_{region_short_name}'],
            )

            records.append(obj)

    return records

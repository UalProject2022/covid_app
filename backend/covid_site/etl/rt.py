import pandas as pd
from covid_site.etl.tools import ETLProcessStatus, run_etl
from covid_site.models import Region, TransmissionRisk
from django.db import transaction

NEW_COLUMN_NAMES = {
    'data': 'reference_date',
    'rt_nacional': 'tr_national',
    'rt_95_inferior_nacional': 'tr_95_lower_national',
    'rt_95_superior_nacional': 'tr_95_upper_national',
    'rt_continente': 'tr_continent',
    'rt_95_inferior_continente': 'tr_95_lower_continent',
    'rt_95_superior_continente': 'tr_95_upper_continent',
    'rt_arsnorte': 'tr_arsnorth',
    'rt_95_inferior_arsnorte': 'tr_95_lower_arsnorth',
    'rt_95_superior_arsnorte': 'tr_95_upper_arsnorth',
    'rt_arscentro': 'tr_arscenter',
    'rt_95_inferior_arscentro': 'tr_95_lower_arscenter',
    'rt_95_superior_arscentro': 'tr_95_upper_arscenter',
    'rt_arslvt': 'tr_arslvt',
    'rt_95_inferior_arslvt': 'tr_95_lower_arslvt',
    'rt_95_superior_arslvt': 'tr_95_upper_arslvt',
    'rt_arsalentejo': 'tr_arsalentejo',
    'rt_95_inferior_arsalentejo': 'tr_95_lower_arsalentejo',
    'rt_95_superior_arsalentejo': 'tr_95_upper_arsalentejo',
    'rt_arsalgarve': 'tr_arsalgarve',
    'rt_95_inferior_arsalgarve': 'tr_95_lower_arsalgarve',
    'rt_95_superior_arsalgarve': 'tr_95_upper_arsalgarve',
    'rt_açores': 'tr_acores',
    'rt_95_inferior_açores': 'tr_95_lower_acores',
    'rt_95_superior_açores': 'tr_95_upper_acores',
    'rt_madeira': 'tr_madeira',
    'rt_95_inferior_madeira': 'tr_95_lower_madeira',
    'rt_95_superior_madeira': 'tr_95_upper_madeira',
}


def rt_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the rt.csv file.

    Args:
        df (pd.DataFrame): the DataFrame loaded from the CSV file.

    Returns:
        ETLProcessStatus: the status of the ETL process, containing the error
            (if any).
    '''
    try:
        df.rename(columns=NEW_COLUMN_NAMES, inplace=True)

        date_columns_formats = {
            'reference_date': f'%Y-%m-%d',
        }

        for c, f in date_columns_formats.items():
            df[c] = pd.to_datetime(df[c], format=f, utc=True)

        run_etl(
            df=df,
            django_model=TransmissionRisk,
            specific_etl_method=generate_transmission_risk_records,
            delete_if_all_none=(
                'transmission_risk',
                'limit_lower',
                'limit_upper'
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
def generate_transmission_risk_records(df: pd.DataFrame) -> list[TransmissionRisk]:
    '''Generates records for the Transmission Risk table according to the
        provided DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[TransmissionRisk]: list of objects to be inserted / updated.
    '''

    regions = Region.objects.all()

    records = list()
    for row in df.to_dict(orient='records'):

        for region in regions.iterator():
            region_short_name = region.short_name

            if region_short_name not in ('foreign',):

                if f'tr_{region_short_name}' in row.keys():
                    transmission_risk = row[f'tr_{region_short_name}']
                    limit_lower = row[f'tr_95_lower_{region_short_name}']
                    limit_upper = row[f'tr_95_upper_{region_short_name}']
                else:
                    transmission_risk = row[f'tr_ars{region_short_name}']
                    limit_lower = row[f'tr_95_lower_ars{region_short_name}']
                    limit_upper = row[f'tr_95_upper_ars{region_short_name}']

                obj = TransmissionRisk(
                    reference_date=row['reference_date'],
                    region=region,
                    transmission_risk=transmission_risk,
                    limit_lower=limit_lower,
                    limit_upper=limit_upper,
                )

                records.append(obj)

    return records

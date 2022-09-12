import pandas as pd
from covid_site.etl.tools import ETLProcessStatus, run_etl
from covid_site.models import Sample
from django.db import transaction

NEW_COLUMN_NAMES = {
    'data': 'reference_date',
    'amostras': 'total',
    'amostras_novas': 'new',
    'amostras_pcr': 'pcr',
    'amostras_pcr_novas': 'pcr_new',
    'amostras_antigenio': 'antigen',
    'amostras_antigenio_novas': 'antigen_new',
}


def amostras_csv_etl(df: pd.DataFrame) -> ETLProcessStatus:
    '''Executes the ETL process for the amostras.csv file.

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
            django_model=Sample,
            specific_etl_method=generate_sample_records,
            delete_if_all_none=(
                'total',
                'new',
                'pcr',
                'pcr_new',
                'antigen',
                'antigen_new',
            )
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
def generate_sample_records(df: pd.DataFrame) -> list[Sample]:
    '''Generates records for the Sample table according to the provided
        DataFrame.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.

    Returns:
        list[Sample]: list of objects to be inserted / updated.
    '''

    records = list()
    for row in df.to_dict(orient='records'):
        records.append(Sample(**row))

    return records

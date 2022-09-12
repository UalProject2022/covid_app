import time
from typing import Callable

import pandas as pd
from django.db import models, transaction


class ETLProcessStatus:
    def __init__(self, succeeded: bool, message: str, exception: Exception = None):
        self.succeeded = succeeded
        self.message = message
        self.exception = exception


def fields_to_dict(django_model_instance: object):
    '''Returns a dictionary of the fields in the given model instance.'''

    columns_to_ignore = ('_state',)
    return {k: v for k, v in django_model_instance.__dict__.items() if k not in columns_to_ignore}


def get_cols_to_update(django_model: models.Model):
    '''Returns the list of columns to update in the given model.'''

    columns_to_ignore = django_model.filter_columns() + (
        'id',
        'inserted_date',
        'updated_date',
    )
    return (f.name for f in django_model._meta.fields if f.name not in columns_to_ignore)


def get_table_cols(django_model: models.Model):
    '''Returns the list of relevant columns in the given model.'''

    columns_to_ignore = ('id', 'inserted_date', 'updated_date')
    return (f.name for f in django_model._meta.fields if f.name not in columns_to_ignore)


@transaction.atomic
def bulk_update_or_create(
        django_model: models.Model,
        records: list[object],
        batch_size: int = 1000,
) -> None:
    '''Filter the records provided to check which needs to be update and which
        needs to be created, and then performs the necessary bulk operations.

    Args:
        django_model (models.Model): the model do update.
        records (list[object]): the list of records to filter.
        batch_size (int, optional): the amount records to update/create each
            time. Defaults to 1000.
    '''

    if not records:
        print('Canceling bulk update or create because there are no new records.')
        return

    start_time = time.time()
    table_name = django_model._meta.verbose_name
    print(f'\nStarting bulk operations for {table_name} table..')

    records_to_create = []
    records_to_update = []

    print(f'Starting to filter now: {(time.time() - start_time):.0f}.')

    for obj in records:
        dict_object = fields_to_dict(obj)

        _filter = {k: v for k, v in dict_object.items(
        ) if k in django_model.filter_columns()}

        queried_obj = django_model.objects.filter(**_filter).first()

        if queried_obj is not None:
            dict_object['id'] = queried_obj.id
            records_to_update.append(dict_object)
        else:
            dict_object.pop('id')
            records_to_create.append(dict_object)

    print(f'Starting to insert now: {(time.time() - start_time):.0f}.')
    created_records = django_model.objects.bulk_create(
        objs=[django_model(**o) for o in records_to_create],
        batch_size=batch_size,
    )
    print(f'created_records: {len(created_records)}')

    print(f'Starting to update now: {(time.time() - start_time):.0f}.')
    updated_records = django_model.objects.bulk_update(
        objs=[django_model(**o) for o in records_to_update],
        fields=get_cols_to_update(django_model),
        batch_size=batch_size,
    )
    print(f'updated_records: {updated_records}')

    spent = time.time() - start_time
    print(f'Updated {table_name} table! Spent: {spent:.0f} seconds on it.')


@transaction.atomic
def run_etl(
    df: pd.DataFrame,
    django_model: models.Model,
    specific_etl_method: Callable,
    delete_if_all_none: tuple[str] = tuple(),
) -> None:
    '''Runs the specified ETL process, performing the necessary bulk operations.

    Args:
        df (pd.DataFrame): the DataFrame from which to extract the data.
        django_model (models.Model): the model to update.
        specific_etl_method (Callable): the method to be called.
        delete_if_all_none (tuple[str], optional): the filter to use when its
            necessary to clean the table after the insert of nullable records.
            Defaults to tuple() - no record will be deleted.
    '''

    start_time = time.time()
    table_name = django_model._meta.verbose_name
    info = f'Starting update of {table_name} table..'
    print(info)

    records = specific_etl_method(df=df)

    bulk_update_or_create(django_model=django_model, records=records)

    if delete_if_all_none:
        django_model.objects.filter(
            **{k: None for k in delete_if_all_none}
        ).delete()

    spent = time.time() - start_time
    print(f'Updated {table_name} table! Spent: {spent:.0f} seconds on it.')

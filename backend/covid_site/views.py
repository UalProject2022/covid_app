import numpy as np
import pandas as pd
from django.contrib import messages
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response

from covid_site.etl.amostras import amostras_csv_etl
from covid_site.etl.dados_sico import dados_sico_csv_etl
from covid_site.etl.data import data_csv_etl
from covid_site.etl.data_concelhos_new import data_concelhos_new_csv_etl
from covid_site.etl.rt import rt_csv_etl
from covid_site.etl.vacinas import vacinas_csv_etl
from covid_site.forms import CsvUploadForm
from covid_site.models import StatisticsByAgeAndSex
from covid_site.serializers import *

# The list of acceptable files on the CSV import functionality
ACCEPTABLE_FILES = [
    'amostras.csv',
    'data_concelhos_new.csv',
    'data.csv',
    'rt.csv',
    'vacinas.csv',
    # Actually for SICO files the pattern needs to match, not the whole name
    'Dados_SICO.csv'
]

# Import functionality


def import_csv(request: object) -> dict:
    '''Functionality to import all the acceptable files.

    Args:
        request (object): the request from django admin.

    Returns:
        dict: the payload with the form.
    '''

    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_name = csv_file.name
        print(f'File inserted: {file_name}')

        if file_name not in ACCEPTABLE_FILES and 'Dados_SICO' not in file_name:
            messages.warning(
                request=request,
                message=f'The {file_name} file does not match any mapped source file!',
            )

        else:
            df = pd.read_csv(csv_file, delimiter=',').fillna(
                np.nan).replace([np.nan], [None])
            messages.success(
                request, f'The {file_name} file was uploaded with success!')

            file_name = file_name.split('.')[0]

            if file_name == 'amostras':
                status = amostras_csv_etl(df=df)
            elif file_name == 'data_concelhos_new':
                status = data_concelhos_new_csv_etl(df=df)
            elif file_name == 'data':
                status = data_csv_etl(df=df)
            elif file_name == 'rt':
                status = rt_csv_etl(df=df)
            elif file_name == 'vacinas':
                status = vacinas_csv_etl(df=df)
            elif 'Dados_SICO' in file_name:
                status = dados_sico_csv_etl(df=df)

            if status.succeeded:
                messages.success(
                    request=request,
                    message='ETL finished with success!',
                )
            else:
                messages.error(
                    request=request,
                    message=str(status.exception),
                )

    form = CsvUploadForm()
    return {'form': form}


# Raw API endpoints

class APIModelQuery:
    '''Generalized class to execute the ORM queries to the database.'''

    def __init__(
        self,
        django_model: models.Model,
        serializer: serializers.ModelSerializer,
    ) -> None:
        '''The constructor of the class.

        Args:
            django_model (models.Model): the model to execute the ORM queries.
            serializer (serializers.ModelSerializer): the serializer of the data.
        '''

        self.django_model = django_model
        self.serializer = serializer

    def query_model(
        self,
        request: object,
        order_fields: tuple[str] = tuple(),
    ) -> list[dict]:
        '''Executes the automatically generated query to the provided model.

        Args:
            request (object): the request from django admin.
            order_fields (tuple[str], optional): the fields to order the
                dataset. Defaults to tuple().

        Returns:
            list[dict]: the array with all the rows of the dataset.
        '''

        data = self.django_model.objects.\
            select_related().\
            filter(**{k: v for k, v in request.query_params.items()}).\
            all().\
            order_by(*order_fields)

        object_serializer = self.serializer(
            data,
            context={'request': request},
            many=True,
        )

        return object_serializer.data


@api_view(['GET'])
def age_list(request: object) -> Response:
    '''Executes a query to the Age model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Age,
        serializer=AgeSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def county_list(request: object) -> Response:
    '''Executes a query to the County model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=County,
        serializer=CountySerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def general_data_list(request: object) -> Response:
    '''Executes a query to the GeneralData model, using the provided fields, if
        any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=GeneralData,
        serializer=GeneralDataSerializer,
    )

    order_fields = (
        'reference_date',
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields,
    )

    return Response(result)


@api_view(['GET'])
def incidence_list(request: object) -> Response:
    '''Executes a query to the Incidence model, using the provided fields, if
        any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Incidence,
        serializer=IncidenceSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def incidence_category_list(request: object) -> Response:
    '''Executes a query to the IncidenceCategory model, using the provided
        fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=IncidenceCategory,
        serializer=IncidenceCategorySerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def population_by_age_list(request: object) -> Response:
    '''Executes a query to the PopulationByAge model, using the provided fields,
        if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=PopulationByAge,
        serializer=PopulationByAgeSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def region_list(request: object) -> Response:
    '''Executes a query to the Region model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Region,
        serializer=RegionSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def reinforcement_list(request: object) -> Response:
    '''Executes a query to the Reinforcement model, using the provided fields,
        if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Reinforcement,
        serializer=ReinforcementSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def sample_list(request: object) -> Response:
    '''Executes a query to the Sample model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Sample,
        serializer=SampleSerializer,
    )

    order_fields = (
        'reference_date',
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields,
    )

    return Response(result)


@api_view(['GET'])
def statistics_by_age_and_sex_list(request: object) -> Response:
    '''Executes a query to the StatisticsByAgeAndSex model, using the provided
        fields, if any. It orders the dataset according to the "reference_date"
        column, descending.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=StatisticsByAgeAndSex,
        serializer=StatisticsByAgeAndSexSerializer,
    )

    order_fields = (
        '-reference_date',
        'age__age_start',
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields,
    )

    return Response(result)


@api_view(['GET'])
def statistics_by_region_list(request: object) -> Response:
    '''Executes a query to the StatisticsByRegion model, using the provided
        fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=StatisticsByRegion,
        serializer=StatisticsByRegionSerializer,
    )

    order_fields = (
        'reference_date',
        'region__name',
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields,
    )

    return Response(result)


@api_view(['GET'])
def statistics_by_sex_list(request: object) -> Response:
    '''Executes a query to the StatisticsBySex model, using the provided fields,
        if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=StatisticsBySex,
        serializer=StatisticsBySexSerializer,
    )

    order_fields = (
        'reference_date',
        'sex'
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields
    )

    return Response(result)


@api_view(['GET'])
def symptoms_list(request: object) -> Response:
    '''Executes a query to the Symptoms model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Symptoms,
        serializer=SymptomsSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def symptoms_type_list(request: object) -> Response:
    '''Executes a query to the SymptomsType model, using the provided fields, if
        any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=SymptomsType,
        serializer=SymptomsTypeSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def total_deaths_list(request: object) -> Response:
    '''Executes a query to the TotalDeaths model, using the provided fields, if
        any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=TotalDeaths,
        serializer=TotalDeathsSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def transmission_risk_list(request: object) -> Response:
    '''Executes a query to the TransmissionRisk model, using the provided
        fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=TransmissionRisk,
        serializer=TransmissionRiskSerializer,
    )

    result = query_engine.query_model(request=request)

    return Response(result)


@api_view(['GET'])
def vaccines_list(request: object) -> Response:
    '''Executes a query to the Vaccines model, using the provided fields, if any.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query_engine = APIModelQuery(
        django_model=Vaccines,
        serializer=VaccinesSerializer,
    )

    order_fields = (
        'reference_date',
    )

    result = query_engine.query_model(
        request=request,
        order_fields=order_fields,
    )

    return Response(result)


# Additional endpoints to be specifically used by the front-end
@api_view(['GET'])
def county_summary_dict(request: object) -> Response:
    '''Executes a query to the County model, with a specific query to return the
        needed data structured to be used by the front-end.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query = '''
        WITH ranked_incidence AS (
            SELECT
                i.*,
                (ROW_NUMBER() OVER (PARTITION BY county_id ORDER BY reference_date DESC)) AS rn
            FROM incidence AS i
        )
        SELECT
            1                       AS id,
            c.county_name           AS county_name,
            c.area                  AS area,
            c.population            AS population,
            c.population_density    AS population_density,
            td.`year`               AS `year`,
            td.year_total_deaths    AS year_total_deaths,
            ri.reference_date       AS reference_date,
            ic.incidence_risk       AS incidence_risk,
            ri.incidence            AS incidence,
            ri.confirmed_1          AS confirmed_1,
            ri.cases_14             AS cases_14
        FROM (
            SELECT
                county_id,
                EXTRACT(YEAR FROM date_start) AS `year`,
                SUM(deaths) AS year_total_deaths
            FROM total_deaths
            WHERE EXTRACT(YEAR FROM date_start) = YEAR(CURDATE())
            GROUP BY
                county_id,
                EXTRACT(YEAR FROM date_start)
        ) AS td
        INNER JOIN ranked_incidence AS ri ON td.county_id = ri.county_id
        INNER JOIN county AS c ON td.county_id = c.id
        INNER JOIN incidence_category ic ON ri.incidence_category_id = ic.id
        WHERE rn = 1
        ORDER BY c.county_name;
    '''

    data = TotalDeaths.objects.raw(raw_query=query)

    object_serializer = CountySummarySerializer(
        data,
        context={'request': request},
        many=True,
    )

    dict_data = dict()
    for county in object_serializer.data:
        dict_data[county['county_name']] = county

    return Response(dict_data)


@api_view(['GET'])
def statistics_by_age_list(request: object) -> Response:
    '''Executes a query to the StatisticsByAgeAndSex model, with a specific
        query to return the needed data structured to be used by the front-end.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query = '''
        SELECT
            1                           AS id,
            CASE
                WHEN age.age_end IS NULL THEN CONCAT(age.age_start, '+')
                ELSE CONCAT(age.age_start, '-', age.age_end)
            END                         AS age_range,
            m.confirmed + f.confirmed   AS cases,
            m.deaths + f.deaths         AS deaths,
            m.reference_date            AS reference_date,
            m.inserted_date             AS inserted_date,
            m.updated_date              AS updated_date
        FROM statistics_by_age_and_sex  AS m
        JOIN statistics_by_age_and_sex  AS f
            ON m.reference_date = f.reference_date
            AND m.sex = 'm' and f.sex = 'f'
            AND m.age_id = f.age_id
        JOIN age ON m.age_id = age.id
        WHERE m.reference_date = (SELECT MAX(reference_date) FROM statistics_by_age_and_sex)
        ORDER BY age_range;
    '''

    data = StatisticsByAgeAndSex.objects.raw(raw_query=query)

    object_serializer = StatisticsByAgeSerializer(
        data,
        context={'request': request},
        many=True,
    )

    summarize = request.query_params.get('summarize')
    all_data = object_serializer.data

    if summarize and summarize.isdigit() and int(summarize):
        threshold = 0.04
        total_deaths = sum([v['deaths'] for v in all_data])

        filtered_data = list()

        others = {
            'reference_date': None,
            'age_range': 'Others',
            'cases': 0,
            'deaths': 0,
            'inserted_date': None,
            'updated_date': None
        }

        for v in all_data:
            if v['deaths']/total_deaths > threshold:
                filtered_data.append(v)
            else:
                others['reference_date'] = v['reference_date']
                others['cases'] += v['cases']
                others['deaths'] += v['deaths']
                others['inserted_date'] = v['inserted_date']
                others['updated_date'] = v['updated_date']

        filtered_data.append(others)

        return Response(filtered_data)

    return Response(all_data)


@api_view(['GET'])
def statistics_by_age_and_sex_combined_list(request: object) -> Response:
    '''Executes a query to the StatisticsByAgeAndSex model, with a specific
        query to return the needed data structured to be used by the front-end.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query = '''
        SELECT
            1                   AS id,
            CASE
                WHEN age.age_end IS NULL THEN CONCAT(age.age_start, '+')
                ELSE CONCAT(age.age_start, '-', age.age_end)
            END                 AS age_range,
            m.confirmed         AS male_confirmed,
            m.deaths            AS male_deaths,
            f.confirmed         AS female_confirmed,
            f.deaths            AS female_deaths,
            m.reference_date    AS reference_date,
            m.inserted_date     AS inserted_date,
            m.updated_date      AS updated_date
        FROM statistics_by_age_and_sex AS m
        JOIN statistics_by_age_and_sex AS f
            ON m.reference_date = f.reference_date
            AND m.sex = 'm' and f.sex = 'f'
            AND m.age_id = f.age_id
        JOIN age ON m.age_id = age.id
        WHERE m.reference_date = (SELECT MAX(reference_date) FROM statistics_by_age_and_sex)
        ORDER BY age_range;
    '''

    data = StatisticsByAgeAndSex.objects.raw(raw_query=query)

    object_serializer = StatisticsByAgeAndSexCombinedSerializer(
        data,
        context={'request': request},
        many=True,
    )

    return Response(object_serializer.data)


@api_view(['GET'])
def statistics_by_region_total_list(request: object) -> Response:
    '''Executes a query to the StatisticsByRegion model, with a specific
        query to return the needed data structured to be used by the front-end.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query = '''
        WITH ranked_statistics_by_region AS (
            SELECT
                sbr.*,
                (ROW_NUMBER() OVER (PARTITION BY sbr.region_id ORDER BY sbr.reference_date DESC)) AS rn
            FROM statistics_by_region AS sbr
        )
        SELECT
            1					AS id,
            r.name				AS region_name,
            s.reference_date	AS reference_date,
            s.confirmed			AS cases,
            s.recovered			AS recovered,
            s.deaths			AS total_covid_deaths,
            gtd.total_deaths	AS total_deaths,
            s.inserted_date		AS inserted_date,
            s.updated_date		AS updated_date
        FROM ranked_statistics_by_region AS s
        JOIN region AS r ON s.region_id = r.id
        JOIN (
            SELECT
                c.region_id,
                SUM(td.deaths) AS total_deaths
            FROM (SELECT * FROM total_deaths WHERE date_start >= (SELECT MIN(reference_date) FROM statistics_by_region)) AS td
            JOIN county AS c ON td.county_id = c.id
            GROUP BY c.region_id
            ) AS gtd ON s.region_id = gtd.region_id
        WHERE rn = 1
            AND r.name != 'Foreign'
        ORDER BY region_name;
    '''

    data = StatisticsByRegion.objects.raw(raw_query=query)

    object_serializer = StatisticsByRegionTotalSerializer(
        data,
        context={'request': request},
        many=True,
    )

    return Response(object_serializer.data)


@api_view(['GET'])
def statistics_by_sex_combined_list(request: object) -> Response:
    '''Executes a query to the StatisticsBySex model, with a specific
        query to return the needed data structured to be used by the front-end.

    Args:
        request (object): the request from django admin.

    Returns:
        Response: the Response containing the JSON-like dataset.
    '''

    query = '''
        SELECT
            1                   AS id,
            m.reference_date    AS reference_date,
            m.confirmed         AS male_confirmed,
            m.deaths            AS male_deaths,
            f.confirmed         AS female_confirmed,
            f.deaths            AS female_deaths,
            m.confirmed_unknown AS confirmed_unknown,
            m.inserted_date     AS inserted_date,
            m.updated_date      AS updated_date
        FROM statistics_by_sex AS m
        JOIN statistics_by_sex AS f
            ON m.reference_date = f.reference_date and m.sex = 'm' and f.sex = 'f'
        ORDER BY m.reference_date;
    '''

    data = StatisticsBySex.objects.raw(raw_query=query)

    object_serializer = StatisticsBySexCombinedSerializer(
        data,
        context={'request': request},
        many=True,
    )

    return Response(object_serializer.data)

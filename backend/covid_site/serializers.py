from rest_framework import serializers

from covid_site.models import (Age, County, GeneralData, Incidence,
                               IncidenceCategory, PopulationByAge, Region,
                               Reinforcement, Sample, StatisticsByAgeAndSex,
                               StatisticsByRegion, StatisticsBySex, Symptoms,
                               SymptomsType, TotalDeaths, TransmissionRisk,
                               Vaccines)

DATE_FORMAT = r'%Y-%m-%d'
DATETIME_FORMAT = r'%Y-%m-%d %H:%M:%S'


class AgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Age
        fields = tuple(f.name for f in model._meta.fields)


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = tuple(f.name for f in model._meta.fields)


class GeneralDataSerializer(serializers.ModelSerializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    release_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = GeneralData
        fields = tuple(f.name for f in model._meta.fields)


class IncidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incidence
        fields = tuple(f.name for f in model._meta.fields)


class IncidenceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IncidenceCategory
        fields = tuple(f.name for f in model._meta.fields)


class PopulationByAgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PopulationByAge
        fields = tuple(f.name for f in model._meta.fields)


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = tuple(f.name for f in model._meta.fields)


class ReinforcementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reinforcement
        fields = tuple(f.name for f in model._meta.fields)


class SampleSerializer(serializers.ModelSerializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Sample
        fields = tuple(f.name for f in model._meta.fields)


class StatisticsByAgeAndSexSerializer(serializers.ModelSerializer):
    age_start = serializers.ReadOnlyField(source='age.age_start')
    age_end = serializers.ReadOnlyField(source='age.age_end')
    age_range = serializers.ReadOnlyField(source='age.age_range')

    class Meta:
        model = StatisticsByAgeAndSex
        additional_fields = (
            'age_start',
            'age_end',
            'age_range',
        )
        fields = tuple(f.name for f in model._meta.fields) + additional_fields


class StatisticsByAgeAndSexCombinedSerializer(serializers.Serializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    age_range = serializers.CharField()
    male_confirmed = serializers.IntegerField()
    male_deaths = serializers.IntegerField()
    female_confirmed = serializers.IntegerField()
    female_deaths = serializers.IntegerField()
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)


class StatisticsByAgeSerializer(serializers.Serializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    age_range = serializers.CharField()
    cases = serializers.IntegerField()
    deaths = serializers.IntegerField()
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)


class StatisticsByRegionSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = StatisticsByRegion
        additional_fields = (
            'region_name',
        )
        fields = tuple(f.name for f in model._meta.fields) + additional_fields


class StatisticsByRegionTotalSerializer(serializers.Serializer):
    region_name = serializers.CharField()
    reference_date = serializers.DateField(format=DATE_FORMAT)
    cases = serializers.IntegerField()
    recovered = serializers.IntegerField()
    total_covid_deaths = serializers.IntegerField()
    total_deaths = serializers.IntegerField()
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)


class StatisticsBySexSerializer(serializers.ModelSerializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = StatisticsBySex
        fields = tuple(f.name for f in model._meta.fields)


class StatisticsBySexCombinedSerializer(serializers.Serializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    male_confirmed = serializers.IntegerField()
    male_deaths = serializers.IntegerField()
    female_confirmed = serializers.IntegerField()
    female_deaths = serializers.IntegerField()
    confirmed_unknown = serializers.IntegerField()
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)


class SymptomsSerializer(serializers.ModelSerializer):
    v_symptoms_type = serializers.ReadOnlyField(source='symptoms_type.type')
    inserted_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Symptoms
        additional_fields = (
            'v_symptoms_type',
        )
        fields = tuple(f.name for f in model._meta.fields) + additional_fields


class SymptomsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomsType
        fields = tuple(f.name for f in model._meta.fields)


class TotalDeathsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TotalDeaths
        fields = tuple(f.name for f in model._meta.fields)


class TransmissionRiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransmissionRisk
        fields = tuple(f.name for f in model._meta.fields)


class VaccinesSerializer(serializers.ModelSerializer):
    reference_date = serializers.DateField(format=DATE_FORMAT)
    updated_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Vaccines
        fields = tuple(f.name for f in model._meta.fields)


class CountySummarySerializer(serializers.Serializer):
    county_name = serializers.CharField()
    area = serializers.FloatField()
    population = serializers.IntegerField()
    population_density = serializers.FloatField()
    year = serializers.IntegerField()
    year_total_deaths = serializers.IntegerField()
    reference_date = serializers.DateField(format=DATE_FORMAT)
    incidence_risk = serializers.CharField()
    incidence = serializers.IntegerField()
    confirmed_1 = serializers.IntegerField()
    cases_14 = serializers.IntegerField()

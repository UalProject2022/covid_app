from django.contrib import admin

from covid_site.models import (Age, County, GeneralData, Incidence,
                               IncidenceCategory, PopulationByAge, Region,
                               Reinforcement, Sample, StatisticsByAgeAndSex,
                               StatisticsByRegion, StatisticsBySex, Symptoms,
                               SymptomsType, TotalDeaths, TransmissionRisk,
                               Vaccines)


@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = (
        'age_start',
        'age_end',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(IncidenceCategory)
class IncidenceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_lower_limit',
        'category_upper_limit',
        'incidence_risk',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = (
        'dicofre',
        'district',
        'county_name',
        'region',
        'area',
        'population',
        'population_density',
        'density_1',
        'density_2',
        'density_3',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(GeneralData)
class GeneralDataAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'release_date',
        'active',
        'confirmed',
        'confirmed_new',
        'confirmed_unknown',
        'not_confirmed',
        'recovered',
        'deaths',
        'interned',
        'interned_icu',
        'interned_infirmary',
        'lab',
        'suspects',
        'vigilance',
        'transmission_chains',
        'transmission_imported',
        'incidence_continent',
        'incidence_national',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'county',
        'incidence_category',
        'incidence',
        'cases_14',
        'confirmed_1',
        'confirmed_14',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(PopulationByAge)
class PopulationByAgeAdmin(admin.ModelAdmin):
    list_display = (
        'age',
        'county',
        'people',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(StatisticsByRegion)
class StatisticsByRegionAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'region',
        'confirmed',
        'deaths',
        'recovered',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Reinforcement)
class ReinforcementAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'age',
        'total',
        'new',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'total',
        'new',
        'pcr',
        'pcr_new',
        'antigen',
        'antigen_new',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(StatisticsByAgeAndSex)
class StatisticsByAgeAndSexAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'sex',
        'confirmed',
        'deaths',
        'age',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(StatisticsBySex)
class StatisticsBySexAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'sex',
        'confirmed',
        'confirmed_unknown',
        'deaths',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Symptoms)
class SymptomsAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'quantity',
        'symptoms_type',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(SymptomsType)
class SymptomsTypeAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(TotalDeaths)
class TotalDeathsAdmin(admin.ModelAdmin):
    list_display = (
        'county',
        'date_start',
        'date_end',
        'deaths',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(TransmissionRisk)
class TransmissionRiskAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'region',
        'transmission_risk',
        'limit_lower',
        'limit_upper',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display


@admin.register(Vaccines)
class VaccinesAdmin(admin.ModelAdmin):
    list_display = (
        'reference_date',
        'doses',
        'doses_new',
        'doses_1',
        'doses_1_new',
        'doses_2',
        'doses_2_new',
        'vaccinated_fully',
        'vaccinated_fully_new',
        'vaccinated_partially',
        'vaccinated_partially_new',
        'inoculated',
        'inoculated_new',
        'inoculated_12_plus',
        'vaccines',
        'vaccines_new',
        'vaccinated_fully_continent',
        'vaccinated_fully_continent_new',
        'reinforcement',
        'reinforce_new',
        'reinforcement_continent',
        'reinforcement_continent_new',
        'flu',
        'flu_new',
        'reinforcement_and_flu_new',
        'vaccination_started_05_11',
        'vaccination_started_05_11_new',
        'vaccination_complete_05_11',
        'vaccination_complete_05_11_new',
        'inserted_date',
        'updated_date',
    )

    list_filter = list_display

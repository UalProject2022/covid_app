'''djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from covid_site import views
from django.contrib import admin
from django.urls import path, re_path

api_urls = {
    # Raw API endpoints
    'age': views.age_list,
    'county': views.county_list,
    'general_data': views.general_data_list,
    'incidence': views.incidence_list,
    'incidence_category': views.incidence_category_list,
    'population_by_age': views.population_by_age_list,
    'region': views.region_list,
    'reinforcement': views.reinforcement_list,
    'sample': views.sample_list,
    'statistics_by_age_and_sex': views.statistics_by_age_and_sex_list,
    'statistics_by_region': views.statistics_by_region_list,
    'statistics_by_sex': views.statistics_by_sex_list,
    'symptoms': views.symptoms_list,
    'symptoms_type': views.symptoms_type_list,
    'total_deaths': views.total_deaths_list,
    'transmission_risk': views.transmission_risk_list,
    'vaccines': views.vaccines_list,

    # Additional endpoints to be specifically used by the front-end
    'county_summary': views.county_summary_dict,
    'statistics_by_age': views.statistics_by_age_list,
    'statistics_by_age_and_sex_combined': views.statistics_by_age_and_sex_combined_list,
    'statistics_by_region_total': views.statistics_by_region_total_list,
    'statistics_by_sex_combined': views.statistics_by_sex_combined_list,
}

urlpatterns = [
    path('admin/', admin.site.urls),
]

for url_api, api_view in api_urls.items():
    url_path = re_path(route=f'^api/{url_api}/$', view=api_view)
    urlpatterns.append(url_path)

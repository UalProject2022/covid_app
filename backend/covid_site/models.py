# Make sure each model has one field with primary_key=True
# Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class Age(models.Model):
    age_start = models.SmallIntegerField()
    age_end = models.SmallIntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'age'
        unique_together = (('age_start', 'age_end',),)

    def age_range(self):
        if self.age_end is None:
            return f'{self.age_start}+'
        return f'{self.age_start}-{self.age_end}'

    def __str__(self):
        return self.age_range()

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'age_start',
            'age_end',
        )


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class County(models.Model):
    dicofre = models.CharField(max_length=4, unique=True)
    district = models.CharField(max_length=60)
    county_name = models.CharField(max_length=60, unique=True)
    region = models.ForeignKey('Region', models.DO_NOTHING)
    area = models.FloatField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    population_density = models.FloatField(blank=True, null=True)
    density_1 = models.FloatField(blank=True, null=True)
    density_2 = models.FloatField(blank=True, null=True)
    density_3 = models.FloatField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'county'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.county_name

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'dicofre',
        )


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GeneralData(models.Model):
    reference_date = models.DateField(unique=True)
    release_date = models.DateTimeField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    confirmed = models.IntegerField(blank=True, null=True)
    confirmed_new = models.IntegerField(blank=True, null=True)
    confirmed_unknown = models.IntegerField(blank=True, null=True)
    not_confirmed = models.IntegerField(blank=True, null=True)
    recovered = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    interned = models.IntegerField(blank=True, null=True)
    interned_icu = models.IntegerField(blank=True, null=True)
    interned_infirmary = models.IntegerField(blank=True, null=True)
    lab = models.IntegerField(blank=True, null=True)
    suspects = models.IntegerField(blank=True, null=True)
    vigilance = models.IntegerField(blank=True, null=True)
    transmission_chains = models.IntegerField(blank=True, null=True)
    transmission_imported = models.IntegerField(blank=True, null=True)
    incidence_continent = models.FloatField(blank=True, null=True)
    incidence_national = models.FloatField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'general_data'
        verbose_name_plural = 'General Data'

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'General Data: {only_date}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
        )


class Incidence(models.Model):
    reference_date = models.DateField()
    county = models.ForeignKey(County, models.DO_NOTHING)
    incidence_category = models.ForeignKey(
        'IncidenceCategory', models.DO_NOTHING)
    incidence = models.IntegerField(blank=True, null=True)
    cases_14 = models.IntegerField(blank=True, null=True)
    confirmed_1 = models.IntegerField(blank=True, null=True)
    confirmed_14 = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'incidence'
        unique_together = (('reference_date', 'county'),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Incidence: {only_date} - {self.county}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'county',
        )


class IncidenceCategory(models.Model):
    category_lower_limit = models.IntegerField()
    category_upper_limit = models.IntegerField(blank=True, null=True)
    incidence_risk = models.CharField(max_length=30, unique=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'incidence_category'
        verbose_name_plural = 'Incidence Categories'

    def __str__(self):
        return self.incidence_risk


class PopulationByAge(models.Model):
    age = models.ForeignKey(Age, models.DO_NOTHING)
    county: County = models.ForeignKey(County, models.DO_NOTHING)
    people = models.IntegerField()
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'population_by_age'
        unique_together = (('age', 'county'),)

    def __str__(self):
        return f'Population by Age: {self.county} - {self.age}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'age',
            'county',
        )


class Region(models.Model):
    name = models.CharField(max_length=60, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.name

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'name',
        )


class Reinforcement(models.Model):
    reference_date = models.DateField()
    age = models.ForeignKey(Age, models.DO_NOTHING)
    total = models.IntegerField(blank=True, null=True)
    new = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'reinforcement'
        unique_together = (('reference_date', 'age'),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Reinforcement: {only_date} - {self.age}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'age',
        )


class Sample(models.Model):
    reference_date = models.DateField(unique=True)
    total = models.IntegerField(blank=True, null=True)
    new = models.IntegerField(blank=True, null=True)
    pcr = models.IntegerField(blank=True, null=True)
    pcr_new = models.IntegerField(blank=True, null=True)
    antigen = models.IntegerField(blank=True, null=True)
    antigen_new = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'sample'
        verbose_name_plural = 'Samples'

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Sample: {only_date}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
        )


class StatisticsByAgeAndSex(models.Model):
    reference_date = models.DateField()
    age = models.ForeignKey(Age, models.DO_NOTHING)
    sex = models.CharField(max_length=1)
    confirmed = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'statistics_by_age_and_sex'
        verbose_name_plural = 'Statistics by Age and Sex'
        unique_together = (('reference_date', 'sex', 'age'),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Statistics by Age and Sex: {only_date} - {self.age} - {self.sex}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'age',
            'sex',
        )


class StatisticsByRegion(models.Model):
    reference_date = models.DateField()
    region = models.ForeignKey(Region, models.DO_NOTHING)
    confirmed = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    recovered = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'statistics_by_region'
        unique_together = (('reference_date', 'region'),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Statistics by Region: {only_date} - {self.region}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'region',
        )


class StatisticsBySex(models.Model):
    reference_date = models.DateField(unique=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    confirmed = models.IntegerField(blank=True, null=True)
    confirmed_unknown = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'statistics_by_sex'
        verbose_name_plural = 'Statistics by Sex'
        unique_together = (('reference_date', 'sex',),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Statistics by Sex: {only_date} - {self.sex}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'sex',
        )


class Symptoms(models.Model):
    reference_date = models.DateField()
    quantity = models.FloatField(blank=True, null=True)
    symptoms_type = models.ForeignKey('SymptomsType', models.DO_NOTHING)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'symptoms'
        verbose_name_plural = 'Symptoms'
        unique_together = (('reference_date', 'symptoms_type',),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Symptoms: {only_date} - {self.symptoms_type}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'symptoms_type',
        )


class SymptomsType(models.Model):
    type = models.CharField(max_length=50, unique=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'symptoms_type'

    def __str__(self):
        return self.type

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'type',
        )


class TotalDeaths(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    date_start = models.DateField()
    date_end = models.DateField()
    deaths = models.IntegerField()
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'total_deaths'
        verbose_name_plural = 'Total Deaths'
        unique_together = (
            ('county', 'date_start',),
            ('county', 'date_end',),
        )

    def __str__(self):
        date_start = f'{self.date_start}'[:10]
        date_end = f'{self.date_end}'[:10]
        return f'Total Deaths: {date_start} - {date_end} - {self.county}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'county',
            'date_start',
            'date_end',
        )


class TransmissionRisk(models.Model):
    reference_date = models.DateField()
    region = models.ForeignKey(Region, models.DO_NOTHING)
    transmission_risk = models.FloatField(blank=True, null=True)
    limit_lower = models.FloatField(blank=True, null=True)
    limit_upper = models.FloatField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'transmission_risk'
        unique_together = (('reference_date', 'region',),)

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Transmission Risk: {only_date} - {self.region}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
            'region',
        )


class Vaccines(models.Model):
    reference_date = models.DateField(unique=True)
    doses = models.IntegerField(blank=True, null=True)
    doses_new = models.IntegerField(blank=True, null=True)
    doses_1 = models.IntegerField(blank=True, null=True)
    doses_1_new = models.IntegerField(blank=True, null=True)
    doses_2 = models.IntegerField(blank=True, null=True)
    doses_2_new = models.IntegerField(blank=True, null=True)
    vaccinated_fully = models.IntegerField(blank=True, null=True)
    vaccinated_fully_new = models.IntegerField(blank=True, null=True)
    vaccinated_partially = models.IntegerField(blank=True, null=True)
    vaccinated_partially_new = models.IntegerField(blank=True, null=True)
    inoculated = models.IntegerField(blank=True, null=True)
    inoculated_new = models.IntegerField(blank=True, null=True)
    inoculated_12_plus = models.IntegerField(blank=True, null=True)
    vaccines = models.IntegerField(blank=True, null=True)
    vaccines_new = models.IntegerField(blank=True, null=True)
    vaccinated_fully_continent = models.IntegerField(blank=True, null=True)
    vaccinated_fully_continent_new = models.IntegerField(blank=True, null=True)
    reinforcement = models.IntegerField(blank=True, null=True)
    reinforce_new = models.IntegerField(blank=True, null=True)
    reinforcement_continent = models.IntegerField(blank=True, null=True)
    reinforcement_continent_new = models.IntegerField(blank=True, null=True)
    flu = models.IntegerField(blank=True, null=True)
    flu_new = models.IntegerField(blank=True, null=True)
    reinforcement_and_flu_new = models.IntegerField(blank=True, null=True)
    vaccination_started_05_11 = models.IntegerField(blank=True, null=True)
    vaccination_started_05_11_new = models.IntegerField(blank=True, null=True)
    vaccination_complete_05_11 = models.IntegerField(blank=True, null=True)
    vaccination_complete_05_11_new = models.IntegerField(blank=True, null=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'vaccines'
        verbose_name_plural = 'Vaccines'

    def __str__(self):
        only_date = f'{self.reference_date}'[:10]
        return f'Vaccines: {only_date}'

    @classmethod
    def filter_columns(cls) -> tuple[str]:
        '''The fields to use as filter on the ETL process.

        Returns:
            tuple[str]: the fields to use as filter
        '''
        return (
            'reference_date',
        )

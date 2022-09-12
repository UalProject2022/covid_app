declare module 'dataTypes' {
	type VaccineDataRecord = {
		reference_date: string,
		doses: number,
		doses_new: number,
		doses_1: number,
		doses_1_new: number,
		doses_2: number,
		doses_2_new: number,
		vaccinated_fully: number,
		vaccinated_fully_new: number,
		vaccinated_partially: number,
		vaccinated_partially_new: number,
		inoculated: number,
		inoculated_new: number,
		inoculated_12_plus: number,
		vaccines: number,
		vaccines_new: number,
		vaccinated_fully_continent: number,
		vaccinated_fully_continent_new: number,
		reinforcement: number,
		reinforce_new: number,
		reinforcement_continent: number,
		reinforcement_continent_new: number,
		flu: number,
		flu_new: number,
		reinforcement_and_flu_new: number,
		vaccination_started_05_11: number,
		vaccination_started_05_11_new: number,
		vaccination_complete_05_11: number,
		vaccination_complete_05_11_new: number,
		inserted_date: string,
		updated_date: string,
	};

	type SampleDataRecord = {
		reference_date: string,
		total: number,
		new: number,
		pcr: number,
		pcr_new: number,
		antigen: number,
		antigen_new: number,
		inserted_date: string,
		updated_date: string,
	};

	type StatisticsBySexCombinedDataRecord = {
		reference_date: string,
		male_confirmed: number,
		male_deaths: number,
		female_confirmed: number,
		female_deaths: number,
		confirmed_unknown: number,
		inserted_date: string,
		updated_date: string,
	};

	type RegionDataRecord = {
		id: number,
		reference_date: string,
		region: number,
		confirmed: number,
		deaths: number,
		recovered: number,
		inserted_date: string,
		updated_date: string,
		region_name: string,
	};

	type StatisticsByAgeAndSexCombinedDataRecord = {
		reference_date: string,
		age_range: string,
		male_confirmed: number,
		male_deaths: number,
		female_confirmed: number,
		female_deaths: number,
		inserted_date: string,
		updated_date: string,
	};

	type SymptomsTableRecord = {
		id: number,
		reference_date: string,
		quantity: number,
		symptoms_type: number,
		inserted_date: string,
		updated_date: string,
		v_symptoms_type: string,
	};

	type GeneralDataTableRecord = {
		id: number,
		reference_date: string,
		release_date: string,
		active: number,
		confirmed: number,
		confirmed_new: number,
		confirmed_unknown: number,
		not_confirmed: number,
		recovered: number,
		deaths: number,
		interned: number,
		interned_icu: number,
		interned_infirmary: number,
		lab: number,
		suspects: number,
		vigilance: number,
		transmission_chains: number,
		transmission_imported: number,
		incidence_continent: number,
		incidence_national: number,
		inserted_date: string,
		updated_date: string,
	};

	type StatisticsByAgeDataRecord = {
		reference_date: string,
		age_range: string,
		cases: number,
		deaths: number,
		inserted_date: string,
		updated_date: string,
	};

	type chartAttributes = {
		name: string,
		dataKey: string,
	};
};

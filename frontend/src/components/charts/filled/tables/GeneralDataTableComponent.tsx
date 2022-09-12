import { GeneralDataTableRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { Column } from 'react-table';
import { fetchData } from '../../../../store/tools';
import { TableComponent } from '../../TableComponent';

export const generalDataTableName = 'COVID-19 Data Summary';

export function GeneralDataTableComponent() {
  const emptyData: GeneralDataTableRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}general_data/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const setColumns: Column<GeneralDataTableRecord>[] = [
    {
      Header: 'Reference Date',
      accessor: 'reference_date',
    },
    {
      Header: 'Release Date',
      accessor: 'release_date',
    },
    {
      Header: 'Active Cases',
      accessor: 'active',
    },
    {
      Header: 'Confirmed',
      accessor: 'confirmed',
    },
    {
      Header: 'Confirmed New',
      accessor: 'confirmed_new',
    },
    {
      Header: 'Confirmed Unknown',
      accessor: 'confirmed_unknown',
    },
    {
      Header: 'Not Confirmed',
      accessor: 'not_confirmed',
    },
    {
      Header: 'Recovered',
      accessor: 'recovered',
    },
    {
      Header: 'Deaths',
      accessor: 'deaths',
    },
    {
      Header: 'Interned',
      accessor: 'interned',
    },
    {
      Header: 'Interned ICU',
      accessor: 'interned_icu',
    },
    {
      Header: 'Interned Infirmary',
      accessor: 'interned_infirmary',
    },
    {
      Header: 'Lab',
      accessor: 'lab',
    },
    {
      Header: 'Suspects',
      accessor: 'suspects',
    },
    {
      Header: 'Vigilance',
      accessor: 'vigilance',
    },
    {
      Header: 'Transmission Chains',
      accessor: 'transmission_chains',
    },
    {
      Header: 'Transmission Imported',
      accessor: 'transmission_imported',
    },
    {
      Header: 'Incidence Continent',
      accessor: 'incidence_continent',
    },
    {
      Header: 'Incidence National',
      accessor: 'incidence_national',
    },
    {
      Header: 'Inserted Date',
      accessor: 'inserted_date',
    },
    {
      Header: 'Updated Date',
      accessor: 'updated_date',
    },
  ];

  return TableComponent(isLoading, apiData, setColumns, generalDataTableName);
}

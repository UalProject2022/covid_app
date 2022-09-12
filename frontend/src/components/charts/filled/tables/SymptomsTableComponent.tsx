import { SymptomsTableRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { Column } from 'react-table';
import { fetchData } from '../../../../store/tools';
import { TableComponent } from '../../TableComponent';

export const symptomsTableName = 'Relative Frequency of Symptoms';

export function SymptomsTableComponent() {
  const emptyData: SymptomsTableRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}symptoms/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const setColumns: Column<SymptomsTableRecord>[] = [
    {
      Header: 'Reference Date',
      accessor: 'reference_date',
    },
    {
      Header: 'Symptoms Type',
      accessor: 'v_symptoms_type',
    },
    {
      Header: 'Quantity',
      accessor: 'quantity',
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

  return TableComponent(isLoading, apiData, setColumns, symptomsTableName);
};

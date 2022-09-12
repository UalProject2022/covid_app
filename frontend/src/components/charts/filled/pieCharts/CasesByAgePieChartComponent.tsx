import { StatisticsByAgeDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { PieChartComponent } from '../../PieChartComponent';


export const casesByAgePieChartName = 'Distribution of Cases According to Age';

export function CasesByAgePieChartComponent() {
  const emptyData: StatisticsByAgeDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}statistics_by_age/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  return PieChartComponent(
    isLoading,
    apiData,
    'cases',
    casesByAgePieChartName,
  );
};

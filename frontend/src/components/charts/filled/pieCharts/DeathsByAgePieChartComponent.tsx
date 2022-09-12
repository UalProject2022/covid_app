import { StatisticsByAgeDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { PieChartComponent } from '../../PieChartComponent';


export const deathsByAgePieChartName = 'Distribution of Deaths According to Age';

export function DeathsByAgePieChartComponent() {
  const emptyData: StatisticsByAgeDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}statistics_by_age/?summarize=1`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  return PieChartComponent(
    isLoading,
    apiData,
    'deaths',
    deathsByAgePieChartName,
  );
};

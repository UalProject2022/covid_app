import {
  chartAttributes,
  StatisticsByAgeAndSexCombinedDataRecord
} from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { BarChartComponent } from '../../BarChartComponent';

export const statisticsByAgeAndSexBarChartName = 'Summary of Cases and Deaths by Age and Sex';

export function StatisticsByAgeAndSexBarChartComponent() {
  const emptyData: StatisticsByAgeAndSexCombinedDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}statistics_by_age_and_sex_combined/?`;

    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const chartAtt: chartAttributes[] = [
    {
      name: 'Male Deaths',
      dataKey: 'male_deaths',
    },
    {
      name: 'Male Cases',
      dataKey: 'male_confirmed',
    },
    {
      name: 'Female Deaths',
      dataKey: 'female_deaths',
    },
    {
      name: 'Female Cases',
      dataKey: 'female_confirmed',
    },
  ];

  return BarChartComponent(
    isLoading,
    apiData,
    chartAtt,
    'age_range',
    statisticsByAgeAndSexBarChartName,
  );
};

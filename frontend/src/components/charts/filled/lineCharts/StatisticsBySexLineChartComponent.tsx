import { chartAttributes, StatisticsBySexCombinedDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { LineChartComponent } from '../../LineChartComponent';


export const statisticsBySexLineChartName = 'Cases and Deaths by Sex';

export function StatisticsBySexLineChartComponent() {
  const emptyData: StatisticsBySexCombinedDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}statistics_by_sex_combined/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const chartAtt: chartAttributes[] = [
    {
      'name': 'Male Cases',
      'dataKey': 'male_confirmed',
    },
    {
      'name': 'Male Deaths',
      'dataKey': 'male_deaths',
    },
    {
      'name': 'Female Cases',
      'dataKey': 'female_confirmed',
    },
    {
      'name': 'Female Deaths',
      'dataKey': 'female_deaths',
    },
    {
      'name': 'Cases of Unknown Sex',
      'dataKey': 'confirmed_unknown',
    },
  ];

  return LineChartComponent(
    isLoading,
    apiData,
    chartAtt,
    'reference_date',
    statisticsBySexLineChartName,
  );
}

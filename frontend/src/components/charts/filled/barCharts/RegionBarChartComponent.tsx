import { chartAttributes, RegionDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { BarChartComponent } from '../../BarChartComponent';

export const regionBarChartName = 'COVID-19 Across Regions';

const useColors = [
  '#f39b40',
  '#1111a1',
  '#515a5a',
];

export function RegionBarChartComponent() {
  const emptyData: RegionDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}statistics_by_region_total/?`;

    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const chartAtt: chartAttributes[] = [
    {
      name: 'COVID-19 deaths',
      dataKey: 'total_covid_deaths',
    },
    {
      name: 'Total deaths since COVID-19',
      dataKey: 'total_deaths',
    },
    {
      name: 'Cases',
      dataKey: 'cases',
    },
  ];

  return BarChartComponent(
    isLoading,
    apiData,
    chartAtt,
    'region_name',
    regionBarChartName,
    useColors,
  );
};

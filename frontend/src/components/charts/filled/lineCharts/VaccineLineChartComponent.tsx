import { chartAttributes, VaccineDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { LineChartComponent } from '../../LineChartComponent';


export const vaccineLineChartName: string = 'Evolution of Vaccination';

export function VaccineLineChartComponent() {
  const emptyData: VaccineDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}vaccines/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const chartAtt: chartAttributes[] = [
    {
      'name': 'reinforcement',
      'dataKey': 'reinforcement',
    },
    {
      'name': 'inoculated',
      'dataKey': 'inoculated',
    },
    {
      'name': 'vaccines',
      'dataKey': 'vaccines',
    },
  ];

  return LineChartComponent(
    isLoading,
    apiData,
    chartAtt,
    'reference_date',
    vaccineLineChartName,
  );
}

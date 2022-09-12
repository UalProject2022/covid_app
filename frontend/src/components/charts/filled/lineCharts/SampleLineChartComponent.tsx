import { chartAttributes, SampleDataRecord } from 'dataTypes';
import { useEffect, useState } from 'react';
import { fetchData } from '../../../../store/tools';
import { LineChartComponent } from '../../LineChartComponent';

export const sampleLineChartName = 'Sample Count';

export function SampleLineChartComponent() {
  const emptyData: SampleDataRecord[] = [];
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}sample/?`;
    const returnedApiData = await fetchData(url);

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, []);

  const chartAtt: chartAttributes[] = [
    {
      name: 'antigen',
      dataKey: 'antigen',
    },
    {
      name: 'pcr',
      dataKey: 'pcr',
    },
    {
      name: 'total',
      dataKey: 'total',
    },
  ];

  return LineChartComponent(
    isLoading,
    apiData,
    chartAtt,
    'reference_date',
    sampleLineChartName
  );
};

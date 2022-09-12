import { chartAttributes, SampleDataRecord, StatisticsBySexCombinedDataRecord, VaccineDataRecord } from 'dataTypes';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import LoadingAnimation from '../ui/LoadingAnimation';
import './ChartComponent.css';
import { colors } from './commonChartColors';


export function LineChartComponent(
  isLoading: boolean,
  data: VaccineDataRecord[] | SampleDataRecord[] | StatisticsBySexCombinedDataRecord[],
  chartAtt: chartAttributes[],
  chartDataKey: string,
  chartName: string,
) {
  const chartElement = document.getElementById('chartDiv');
  chartElement?.scrollIntoView({ behavior: 'smooth' });
  return (
    <div
      id='chartDiv' className='chartWrapper'
    >
      {
        isLoading ?

          <div><LoadingAnimation /></div> :

          <>
            <div className='title'>{chartName}</div>

            <ResponsiveContainer width='60%' height={500}>
              <LineChart
                width={1100}
                height={500}
                data={data}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray='3 3' />
                <XAxis dataKey={chartDataKey} />
                <YAxis />
                <Tooltip />
                <Legend />

                {
                  chartAtt.map((line, index) => {
                    return (
                      <Line
                        connectNulls
                        name={line.name}
                        key={`line_${line.name}`}
                        type='monotone'
                        dataKey={line.dataKey}
                        stroke={colors[index]}
                        dot={false}
                      />)
                  })
                }

              </LineChart>
            </ResponsiveContainer>

            <div>Update at {data[0].updated_date}.</div>

          </>

      }

    </div>
  )

};

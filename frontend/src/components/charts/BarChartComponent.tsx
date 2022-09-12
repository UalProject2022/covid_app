import {
  chartAttributes,
  RegionDataRecord,
  StatisticsByAgeAndSexCombinedDataRecord
} from 'dataTypes';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';
import LoadingAnimation from '../ui/LoadingAnimation';
import './ChartComponent.css';
import { colors } from './commonChartColors';

export function BarChartComponent(
  isLoading: boolean,
  data: RegionDataRecord[] | StatisticsByAgeAndSexCombinedDataRecord[],
  chartAtt: chartAttributes[],
  charDataKey: string,
  chartName: string,
  useColors: string[] = colors
) {
  const chartElement = document.getElementById('chartDiv');
  chartElement?.scrollIntoView({ behavior: 'smooth' });
  return (
    <div id='chartDiv' className='chartWrapper'>
      {isLoading ? (
        <div>
          <LoadingAnimation />
        </div>
      ) : (
        <>
          <div className='title'>{chartName}</div>

          <ResponsiveContainer width='60%' height={500}>
            <BarChart
              data={data}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray='3 3' />
              <XAxis dataKey={charDataKey} />
              <YAxis />
              <Tooltip />
              <Legend />

              {chartAtt.map((bar, index) => {
                return (
                  <Bar
                    name={bar.name}
                    key={`bar_${bar.name}`}
                    dataKey={bar.dataKey}
                    fill={useColors[index]}
                  />
                );
              })}
            </BarChart>
          </ResponsiveContainer>

          <div>
            Reference date {data[1].reference_date}. Update at{' '}
            {data[0].updated_date}.
          </div>
        </>
      )}
    </div>
  );
};

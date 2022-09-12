import { StatisticsByAgeDataRecord } from 'dataTypes';
import { Cell, Pie, PieChart, ResponsiveContainer, Sector } from 'recharts';
import LoadingAnimation from '../ui/LoadingAnimation';
import './ChartComponent.css';
import { colors } from './commonChartColors';

const COLORS = [
  '#0088FE',
  '#00C49F',
  '#FFBB28',
  '#FF8042',
  ...colors
]

const renderCustomizedLabel = (props: any) => {
  const RADIAN = Math.PI / 180;
  const {
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
    payload,
    percent,
    value,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';
  const radius = innerRadius + (outerRadius - innerRadius) * 0.6;

  return (
    <g>

      {/* External sector */}
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />

      {/* Path to the name of the sector */}
      <path
        d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
        stroke={fill}
        fill='none'
      />

      {/* Circle at the end of the path */}
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke='none' />

      {/* Name of the sector */}
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        textAnchor={textAnchor}
        fill='#333'
      >{payload.age_range}</text>

      {/* Value of the sector */}
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={18}
        textAnchor={textAnchor}
        fill='#999'
      >{`(${value})`}</text>

      {/* The value (in %) of the sector, loaded inside the slice of the pie */}
      <text
        x={cx + radius * Math.cos(-midAngle * RADIAN)}
        y={cy + radius * Math.sin(-midAngle * RADIAN)}
        fill='white'
        textAnchor='middle'
        dominantBaseline='central'
      >{`${(percent * 100).toFixed(0)}%`}</text>

    </g>

  );
};

export function PieChartComponent(
  isLoading: boolean,
  data: StatisticsByAgeDataRecord[],
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

            <ResponsiveContainer width='50%' aspect={2} >

              <PieChart
                width={400}
                height={400}
                margin={{
                  top: 0,
                  right: 0,
                  bottom: 0,
                  left: 0
                }}
              >

                <Pie
                  data={data}
                  cx='50%'
                  cy='50%'
                  labelLine={false}
                  label={renderCustomizedLabel}
                  outerRadius={140}
                  fill='#8884d8'
                  dataKey={chartDataKey}
                  nameKey='age_range'
                >
                  {
                    data.map(
                      (_entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      )
                    )
                  }
                </Pie>

              </PieChart>

            </ResponsiveContainer>

            <div>Update at {data[0].updated_date}.</div>

          </>

      }

    </div>
  );
};

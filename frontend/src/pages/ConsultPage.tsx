import React, { useState } from 'react';
import { RegionBarChartComponent, regionBarChartName } from '../components/charts/filled/barCharts/RegionBarChartComponent';
import { StatisticsByAgeAndSexBarChartComponent, statisticsByAgeAndSexBarChartName } from '../components/charts/filled/barCharts/StatisticsByAgeAndSexBarChartComponent';
import { SampleLineChartComponent, sampleLineChartName } from '../components/charts/filled/lineCharts/SampleLineChartComponent';
import { StatisticsBySexLineChartComponent, statisticsBySexLineChartName } from '../components/charts/filled/lineCharts/StatisticsBySexLineChartComponent';
import { VaccineLineChartComponent, vaccineLineChartName } from '../components/charts/filled/lineCharts/VaccineLineChartComponent';

import { GeneralDataTableComponent, generalDataTableName } from '../components/charts/filled/tables/GeneralDataTableComponent';
import { SymptomsTableComponent, symptomsTableName } from '../components/charts/filled/tables/SymptomsTableComponent';

import { CasesByAgePieChartComponent, casesByAgePieChartName } from '../components/charts/filled/pieCharts/CasesByAgePieChartComponent';
import { DeathsByAgePieChartComponent, deathsByAgePieChartName } from '../components/charts/filled/pieCharts/DeathsByAgePieChartComponent';
import Accordion from '../components/ui/Accordion';
import classes from './ConsultPage.module.css';


export function ConsultPage() {
  const [selectedRadioBtn, setSelectedRadioBtn] = useState('');
  const isRadioSelected = (value: string): boolean =>
    selectedRadioBtn === value;

  const handleRadioClick = (e: React.ChangeEvent<HTMLInputElement>): void => {
    setSelectedRadioBtn(e.currentTarget.value);
    setIsShown(false);
  };

  const getChartType = (chartName: string): JSX.Element => {
    const charts: { [key: string]: JSX.Element } = {
      // Tables
      'GeneralDataTable': <GeneralDataTableComponent />,
      'SymptomsTable': <SymptomsTableComponent />,

      // Line Charts
      'VaccineLineChart': <VaccineLineChartComponent />,
      'SampleLineChart': <SampleLineChartComponent />,
      'StatisticsBySexLineChart': <StatisticsBySexLineChartComponent />,

      // Bar Charts
      'RegionBarChart': <RegionBarChartComponent />,
      'StatisticsByAgeAndSexBarChart': <StatisticsByAgeAndSexBarChartComponent />,
      'RegionBarChart3': <RegionBarChartComponent />,

      // Pie Charts
      'CasesByAgePieChart': <CasesByAgePieChartComponent />,
      'DeathsByAgePieChart': <DeathsByAgePieChartComponent />,
    }

    return charts[chartName];
  };

  function radioButton(chartType: string, label: string) {
    return (
      <label className={classes.radioContainer}>{label}
        <input
          type='radio'
          name='charts'
          value={chartType}
          checked={isRadioSelected(chartType)}
          onChange={handleRadioClick}
        ></input>
        <span className={classes.checkmark}></span>
      </label>
    );
  }

  //Consult Button Handle
  const [isShown, setIsShown] = useState(false);
  const handleClick = () => { setIsShown(true); };


  const accordionItems = [
    {
      title: 'Tabular data',
      content: (
        <div className={classes.chartRadio}>
          <div>{radioButton('GeneralDataTable', generalDataTableName)}</div>
          <div>{radioButton('SymptomsTable', symptomsTableName)}</div>
        </div>
      ),
    },
    {
      title: 'Line Charts',
      content: (
        <div className={classes.chartRadio}>
          <div>{radioButton('VaccineLineChart', vaccineLineChartName)}</div>
          <div>{radioButton('SampleLineChart', sampleLineChartName)}</div>
          <div>{radioButton('StatisticsBySexLineChart', statisticsBySexLineChartName)}</div>
        </div>
      ),
    },
    {
      title: 'Bar Charts',
      content: (
        <div className={classes.chartRadio}>
          <div>{radioButton('RegionBarChart', regionBarChartName)}</div>
          <div>{radioButton('StatisticsByAgeAndSexBarChart', statisticsByAgeAndSexBarChartName)}</div>
        </div>
      ),
    },
    {
      title: 'Pie Charts',
      content: (
        <div className={classes.chartRadio}>
          <div>{radioButton('CasesByAgePieChart', casesByAgePieChartName)}</div>
          <div>{radioButton('DeathsByAgePieChart', deathsByAgePieChartName)}</div>
        </div>
      ),
    },
  ];

  return (
    <div className={classes.ConsultPage}>
      <h1 className={classes.h1}>Consult</h1>
      <div className={classes.accordion}>
        <Accordion items={accordionItems} />
        <button className={classes.consultBtn} onClick={handleClick}>
          Consult
        </button>
        {isShown && getChartType(selectedRadioBtn)}
      </div>
    </div>
  );
}

import classes from './Welcome.module.css';

export default function Welcome() {
  return (
    <div className={classes.welcome}>
      <div className={classes.card}>
        <h4>Welcome to Covid Site!</h4>
        <p>This website was created by the students of Universidade Autónoma de Lisboa (UAL) as a final end-of-course project.</p>
        <p>The purpose of the project is to create an application for data integration on COVID-19, and this website serves as the frontend of the app,
          providing to the user a demonstration of what is possible to view and also an analysis on the impact of the virus in Portugal.</p>
        <p>It allows the user to view predetermined charts for analysis as well as an interactive map of Portugal with general data on each county.</p>
        <p>All data were gathered through these sources:</p>
        <ul>
          <li>Data related to COVID-19: <a href='https://github.com/dssg-pt/covid19pt-data'>https://github.com/dssg-pt/covid19pt-data</a></li>
          <li>Data related to population deaths: <a href='https://evm.min-saude.pt/#shiny-tab-q_concelhos'>https://evm.min-saude.pt/#shiny-tab-q_concelhos</a></li>
          <li>Geographic data: <a href='https://dados.gov.pt/pt/datasets/concelhos-de-portugal/'>https://dados.gov.pt/pt/datasets/concelhos-de-portugal/</a></li>
        </ul>
      </div>
    </div>
  );

}

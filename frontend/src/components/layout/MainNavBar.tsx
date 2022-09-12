import { Link } from 'react-router-dom';
import classes from './MainNavBar.module.css';


export function MainNavBar() {
  return (
    <header className={classes.header}>
      <div className={classes.logo}>
        <img className={classes.imgLogo} src='/logo.png' width='120' height='120'></img>
        <div className={classes.homeBtn}><Link to='/'><strong>Covid Site</strong></Link></div>
      </div>
      <nav>
        <ul>
          <li>
            <Link to='/'>Home</Link>
          </li>
          <li>
            <Link to='/map'>Map</Link>
          </li>
          <li>
            <Link to='/consult'>Consult</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

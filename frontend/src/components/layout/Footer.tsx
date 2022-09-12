import { Snackbar } from '@material-ui/core';
import { useState } from 'react';
import { BiEnvelope, BiWorld } from 'react-icons/bi';
import { FiCopy } from 'react-icons/fi';
import classes from './Footer.module.css';

export function Footer() {
  const [open, setOpen] = useState(false);

  return (
    <div className={classes.footer}>
      <div className={classes.content}>
        <p className={classes.pContentLogo}>
          <i>Powered by:</i>
          <a href='https://autonoma.pt/'>
            <img src='/ual_logo.jpg' width='110'></img>
          </a>
        </p>
        <div className={classes.divInfo}>
          Covid Site
          <p className={classes.pContentInfo}>
            Universidade Autónoma de Lisboa - Computer Science and Engineering
            Project Lab. Course
          </p>
        </div>
        <div>
          About us
          <p className={classes.pContentPfP}>
            <a href='https://www.linkedin.com/in/bruno-teodoro-7161aaa/'>
              <img
                className={classes.imgPfp}
                src='/bruno_pfp.jpg'
                width='75'
              ></img>
            </a>
            <a href='https://www.linkedin.com/in/david-arco-646703217/'>
              <img
                className={classes.imgPfp}
                src='/david_pfp.jpg'
                width='75'
              ></img>
            </a>
            <a href='https://www.linkedin.com/in/osoaresdiego/'>
              <img
                className={classes.imgPfp}
                src='/diego_pfp.jpg'
                width='75'
              ></img>
            </a>
          </p>
        </div>
        <div>
          Contact
          <div className={classes.divContact}>
            <p>
              <a href='https://www.google.pt/maps/place/Universidade+Aut%C3%B3noma+de+Lisboa/@38.7245489,-9.1479253,17z/data=!3m1!4b1!4m5!3m4!1s0xd193377e3a1fa0b:0xf8ed48982a078932!8m2!3d38.7245447!4d-9.1457366'>
                <BiWorld />
                &nbsp;Palácio Dos Condes Do Redondo, R. de Santa Marta 56,
                1169-023 Lisboa
              </a>
            </p>
            <p className='pEmail'>
              <span>
                <BiEnvelope />
                &nbsp;ual.lab.project2022@gmail.com
                <button
                  className={classes.copyBtn}
                  onClick={() => {
                    setOpen(true);
                    navigator.clipboard.writeText(
                      'ual.lab.project2022@gmail.com'
                    );
                  }}
                >
                  <FiCopy />
                </button>
              </span>
            </p>
            <Snackbar
              open={open}
              onClose={() => setOpen(false)}
              autoHideDuration={2000}
              message='Copied to clipboard'
            />
          </div>
        </div>
      </div>
      <hr className={classes.hr}></hr>
      <div className={classes.copyright}>
        &copy;{new Date().getFullYear()} All rights reserved
      </div>
    </div>
  );
};

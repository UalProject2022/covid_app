import { ReactNode } from 'react';
import { Footer } from './Footer';
import classes from './Layout.module.css';
import { MainNavBar } from './MainNavBar';


type LayoutProps = {
  children: ReactNode;
};

export function Layout(props: LayoutProps) {
  return (
    <div>
      <MainNavBar />
      <main className={classes.main}>{props.children}</main>
      <Footer />
    </div>
  )
};

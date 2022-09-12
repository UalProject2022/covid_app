import { useState } from 'react';
import classes from './Accordion.module.css';
import { AccordionData } from './AccordionData';
import AccordionItem from './AccordionItem';


export default function Accordion({ items }: { items: Array<AccordionData> }) {
  const [currentIndex, setCurrentIndex] = useState(-1);
  const btnOnClick = (index: number) => {
    setCurrentIndex((currentValue) =>
      currentValue !== index ? index : -1);
  }

  return (
    <ul className={classes.accordion}>
      {
        items.map((item, index) => (
          <AccordionItem
            data={item}
            key={index}
            isOpen={index === currentIndex}
            btnOnClick={() => btnOnClick(index)}
          />
        ))}
    </ul>
  );
}

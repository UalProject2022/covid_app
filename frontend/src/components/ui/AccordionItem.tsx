import { useEffect, useRef, useState } from 'react';
import { AccordionData } from './AccordionData';
import './AccordionItem.css';

export default function ({
  data,
  isOpen,
  btnOnClick,
}: {
  data: AccordionData,
  isOpen: boolean
  btnOnClick: () => void
}) {
  const contentRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (isOpen) {
      const contentElement = contentRef.current as HTMLDivElement;
      setHeight(contentElement.scrollHeight)
    } else {
      setHeight(0);
    }
  }, [isOpen]);

  return (
    <li className={`accordionItem ${isOpen ? 'active' : ''}`}>
      <h2 className='accordionItemTitle'>
        <button className='accordionItemButton' onClick={btnOnClick}>
          {data.title}
        </button>
      </h2>
      <div className='accordionItemContainer' style={{ height }}>
        <div ref={contentRef} className='accordionItemContent'>
          {data.content}
        </div>
      </div>
    </li>
  );
}

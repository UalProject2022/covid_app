import { useEffect, useState } from 'react';
import { BsFillArrowUpSquareFill } from 'react-icons/bs';


export default function BackToTop() {
  const [backToTopBtn, setBackToTopBtn] = useState(false);

  useEffect(() => {
    window.addEventListener('scroll', () => {
      const backToTopBtnElement = document.getElementById('backToTopBtn');
      if (window.scrollY > 1100) {
        setBackToTopBtn(true)
      } else {
        setBackToTopBtn(false)
      };
      if (backToTopBtnElement != null) {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 250) {
          backToTopBtnElement.style.paddingBottom = `${250 - (document.body.offsetHeight - window.innerHeight - window.scrollY)}px`;
        } else {
          backToTopBtnElement.style.paddingBottom = 'none';
        }
      }
    })
  }, [])

  const scrollUp = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  return (
    <div>
      {backToTopBtn && (
        <button id='backToTopBtn'
          style={{
            position: 'fixed',
            bottom: '80px',
            right: '80px',
            border: '0',
            height: '35px',
            width: '35px',
            fontSize: '50px',
            cursor: 'pointer',
            backgroundColor: 'transparent'
          }}
          onClick={scrollUp}>
          <BsFillArrowUpSquareFill /><p style={{
            fontSize: '20px',
            width: '60px',
            marginTop: '-5px',
          }}>
            To Top</p></button>
      )}
    </div>
  )
}

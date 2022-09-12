// Import Swiper React components
import { Swiper, SwiperSlide } from 'swiper/react';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import './Carousel.css';

// import required modules
import { Autoplay, Navigation, Pagination } from 'swiper';

export default function Carousel() {
  return (
    <div className='carousel'>
      <Swiper
        loop={true}
        speed={600}
        spaceBetween={30}
        centeredSlides={true}
        autoplay={{
          delay: 6500,
          disableOnInteraction: false,
        }}
        pagination={{
          clickable: true,
        }}
        navigation={true}
        modules={[Autoplay, Pagination, Navigation]}
      >
        <SwiperSlide><img src='/img1.jpg'></img></SwiperSlide>
        <SwiperSlide><img src='/img2.jpg'></img></SwiperSlide>
        <SwiperSlide><img src='/img3.jpg'></img></SwiperSlide>
        <SwiperSlide><img src='/img4.jpg'></img></SwiperSlide>
      </Swiper>
    </div>
  );
}

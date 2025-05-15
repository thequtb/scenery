'use client'

import { useState, useEffect } from "react";
import Link from "next/link";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper";
import Image from "next/image";

const ApiDestinations = () => {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/destinations/');
        
        if (!response.ok) {
          throw new Error(`Error fetching destinations: ${response.status}`);
        }
        
        const data = await response.json();
        setDestinations(data);
        setLoading(false);
      } catch (err) {
        console.error("Failed to fetch destinations:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  if (loading) {
    return <div className="text-center py-50">Loading destinations...</div>;
  }

  if (error) {
    return <div className="text-center py-50 text-red-1">Error: {error}</div>;
  }

  return (
    <>
      <Swiper
        spaceBetween={30}
        className="overflow-visible"
        modules={[Navigation]}
        navigation={{
          nextEl: ".js-api-desti-next",
          prevEl: ".js-api-desti-prev",
        }}
        breakpoints={{
          540: {
            slidesPerView: 2,
            spaceBetween: 20,
          },
          768: {
            slidesPerView: 2,
            spaceBetween: 22,
          },
          1024: {
            slidesPerView: 3,
          },
          1200: {
            slidesPerView: 6,
          },
        }}
      >
        {destinations.map((item) => (
          <SwiperSlide key={item.id}>
            <Link
              href="#"
              className="citiesCard -type-2"
              data-aos="fade"
              data-aos-delay={(item.id % 10) * 100}
            >
              <div className="citiesCard__image rounded-4 ratio ratio-1:1">
                <Image
                  width={191}
                  height={191}
                  className="img-ratio rounded-4 js-lazy"
                  src={item.image || "/img/destinations/placeholder.png"}
                  alt={item.name || "Destination"}
                />
              </div>
              <div className="citiesCard__content mt-10">
                <h4 className="text-18 lh-13 fw-500 text-dark-1 text-capitalize">
                  {item.name || item.location || "Unknown Location"}
                </h4>
                <div className="text-14 text-light-1">
                  {item.properties || item.numberOfProperties || "0"} properties
                </div>
              </div>
            </Link>
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Start navigation button for next prev slide */}
      <button className="section-slider-nav -prev flex-center bg-white text-dark-1 size-40 rounded-full shadow-1 sm:d-none js-api-desti-prev">
        <i className="icon icon-chevron-left text-12" />
      </button>
      <button className="section-slider-nav -next flex-center bg-white text-dark-1 size-40 rounded-full shadow-1 sm:d-none js-api-desti-next">
        <i className="icon icon-chevron-right text-12" />
      </button>
      {/* End navigation button for next prev slide */}
    </>
  );
};

export default ApiDestinations; 
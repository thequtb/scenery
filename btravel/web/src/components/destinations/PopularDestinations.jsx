'use client'

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper";
import { Scrollbar } from "swiper";

const PopularDestinations = () => {
  const [destinations, setDestinations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Default placeholder image to use when image URL is invalid
  const defaultImageUrl = "/img/destinations/1/1.png";

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        // Use relative URL for API endpoint and match route.js path
        const response = await fetch('/api/destinations');
        if (!response.ok) {
          throw new Error(`Failed to fetch destinations: ${response.status}`);
        }
        
        const responseData = await response.json();
        console.log('PopularDestinations API response:', responseData);
        
        // Check if data exists in the response
        if (!responseData || !responseData.data) {
          throw new Error('Invalid data format received from API');
        }
        
        const dataArray = responseData.data;
        
        // Make sure we have an array of destinations
        if (!Array.isArray(dataArray)) {
          throw new Error('API did not return an array of destinations');
        }
        
        // Transform API data to match the component's expected format for popular destinations
        const formattedDestinations = dataArray.map(dest => ({
          id: dest.id,
          city: dest.city || dest.name || 'Unknown City',
          hoverText: dest.hover_text || `${dest.properties || '10'} Properties Available`,
          img: isValidImageUrl(dest.img) ? dest.img : '/img/destinations/1/1.png'
        }));
        
        setDestinations(formattedDestinations);
      } catch (error) {
        console.error('Error fetching popular destinations:', error);
        setError(error.message);
        
        // Fallback to hard-coded data
        setDestinations([
          {
            id: 1,
            city: "New York",
            hoverText: "14 Hotel - 22 Cars - 18 Tours - 95 Activity",
            img: "/img/destinations/1/1.png",
          },
          {
            id: 2,
            city: "London",
            hoverText: "14 Hotel - 22 Cars - 18 Tours - 95 Activity",
            img: "/img/destinations/1/2.png",
          },
          {
            id: 3,
            city: "Barcelona",
            hoverText: "14 Hotel - 22 Cars - 18 Tours - 95 Activity",
            img: "/img/destinations/1/3.png",
          },
          {
            id: 4,
            city: "Sydney",
            hoverText: "14 Hotel - 22 Cars - 18 Tours - 95 Activity",
            img: "/img/destinations/1/4.png",
          },
          {
            id: 5,
            city: "Rome",
            hoverText: "14 Hotel - 22 Cars - 18 Tours - 95 Activity",
            img: "/img/destinations/1/5.png",
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  // Function to check if a URL is a valid image URL
  const isValidImageUrl = (url) => {
    if (!url) return false;
    
    // Basic check for URL format
    try {
      new URL(url);
    } catch (e) {
      // If the URL is a relative path starting with '/'
      if (url.startsWith('/')) {
        return true;
      }
      return false;
    }
    
    // Exclude Google Drive folder links which aren't direct image links
    if (url.includes('drive.google.com/drive') || url.includes('drive.google.com/folders')) {
      return false;
    }
    
    return true;
  };

  // Function to handle image loading errors
  const handleImageError = (e) => {
    e.target.src = defaultImageUrl;
  };

  if (isLoading) {
    return <div className="text-center py-40">Loading destinations...</div>;
  }

  if (error) {
    return <div className="text-center py-40 text-danger">Error: {error}</div>;
  }

  if (destinations.length === 0) {
    return <div className="text-center py-40">No destinations available</div>;
  }

  return (
    <>
      <Swiper
        spaceBetween={30}
        className="overflow-visible"
        scrollbar={{
          el: ".js-popular-destination-scrollbar",
          draggable: true,
        }}
        modules={[Scrollbar, Navigation]}
        navigation={{
          nextEl: ".js-destination-next",
          prevEl: ".js-destination-prev",
        }}
        breakpoints={{
          500: {
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
            slidesPerView: 4,
          },
        }}
      >
        {destinations.map((item) => (
          <SwiperSlide key={item.id}>
            <Link
              href="#"
              className="citiesCard -type-1 d-block rounded-4"
              key={item.id}
            >
              <div className="citiesCard__image ratio ratio-3:4">
                <Image
                  width={300}
                  height={400}
                  src={item.img}
                  alt={item.city}
                  className="js-lazy"
                  onError={handleImageError}
                  unoptimized={!item.img.startsWith('/')} // Skip optimization for external URLs
                />
              </div>
              <div className="citiesCard__content d-flex flex-column justify-between text-center pt-30 pb-20 px-20">
                <div className="citiesCard__bg" />
                <div className="citiesCard__top">
                  <div className="text-14 text-white">{item.hoverText}</div>
                </div>
                <div className="citiesCard__bottom">
                  <h4 className="text-26 md:text-20 lh-13 text-white mb-20">
                    {item.city}
                  </h4>
                  <button className="button col-12 h-60 -blue-1 bg-white text-dark-1">
                    Discover
                  </button>
                </div>
              </div>
            </Link>
          </SwiperSlide>
        ))}
      </Swiper>

      <div>
        <button className="section-slider-nav  -prev flex-center button -blue-1 bg-white shadow-1 size-40 rounded-full sm:d-none js-destination-prev">
          <i className="icon icon-chevron-left text-12" />
        </button>
        <button className="section-slider-nav -next flex-center button -blue-1 bg-white shadow-1 size-40 rounded-full sm:d-none js-destination-next">
          <i className="icon icon-chevron-right text-12" />
        </button>
        <div className="slider-scrollbar bg-light-2 mt-40  js-popular-destination-scrollbar" />
      </div>
    </>
  );
};

export default PopularDestinations;

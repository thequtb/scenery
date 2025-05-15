'use client'

import Link from "next/link";
import { useEffect, useState } from "react";

const Destinations = () => {
  const [filterOption, setFilterOption] = useState("all");
  const [filteredItems, setFilteredItems] = useState([]);
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const filterOptions = [
    { label: "All", value: "all" },
    { label: "Europe", value: "europe" },
    { label: "Asia", value: "asia" },
    { label: "North America", value: "north_america" },
    // add more options as needed
  ];

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch('/api/destinations');
        if (!response.ok) {
          throw new Error(`Failed to fetch destinations: ${response.status}`);
        }
        
        const responseData = await response.json();
        console.log('API Response:', responseData); // Debug log
        
        // Check if data exists in the response
        if (!responseData || !responseData.data) {
          throw new Error('Invalid data format received from API');
        }
        
        // Get the data array
        const dataArray = responseData.data;
        
        if (!Array.isArray(dataArray) || dataArray.length === 0) {
          throw new Error('No destinations found in API response');
        }
        
        // Transform API data to match expected format
        const formattedDestinations = dataArray.map(dest => {
          // Map region names to lowercase for filtering
          let region = 'other';
          if (dest.region) {
            region = dest.region.toLowerCase();
          } else if (dest.country) {
            const country = dest.country.toLowerCase();
            if (['usa', 'united states', 'canada'].includes(country)) {
              region = 'north_america';
            } else if (['uk', 'united kingdom', 'france', 'italy', 'spain', 'germany'].includes(country)) {
              region = 'europe';
            } else if (['japan', 'china', 'thailand', 'india', 'indonesia'].includes(country)) {
              region = 'asia';
            }
          }
          
          return {
            id: dest.id || Math.random().toString(36).substr(2, 9),
            city: dest.city || dest.name || dest.title || 'Unknown',
            properties: dest.properties || 10, // Use 10 as default if null
            region: region
          };
        });
        
        console.log('Formatted destinations:', formattedDestinations);
        setDestinations(formattedDestinations);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching destinations:', error);
        setError(error.message);
        
        // Fallback to hard-coded data if API fails
        import("../../../data/desinations").then(module => {
          setDestinations(module.destinations1);
          setLoading(false);
        }).catch(fallbackError => {
          console.error('Failed to load fallback data:', fallbackError);
          setError('Could not load destinations data');
          setLoading(false);
        });
      }
    };

    fetchDestinations();
  }, []);

  useEffect(() => {
    if (filterOption === 'all') {
      setFilteredItems(destinations);
    } else {
      setFilteredItems(destinations.filter((elm) => elm.region === filterOption));
    }
  }, [filterOption, destinations]);
  
  return (
    <>
      <div className="tabs__controls d-flex js-tabs-controls">
        {filterOptions.map((option) => (
          <div key={option.value}>
            <button
              className={`tabs__button fw-500 text-15 px-30 py-15 rounded-4 js-tabs-button ${
                filterOption === option.value ? "is-tab-el-active" : ""
              }`}
              onClick={() => setFilterOption(option.value)}
            >
              {option.label}
            </button>
          </div>
        ))}
      </div>

      <div className="tabs__content pt-30 js-tabs-content">
        <div className="tabs__pane -tab-item-1 is-tab-el-active">
          {loading ? (
            <div className="row y-gap-20 justify-center">
              <div className="spinner-border text-blue-1" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : error ? (
            <div className="row y-gap-20 justify-center">
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            </div>
          ) : filteredItems.length === 0 ? (
            <div className="row y-gap-20 justify-center">
              <div className="text-center">No destinations found for this region.</div>
            </div>
          ) : (
            <div className="row y-gap-20">
              {filteredItems.map((item) => (
                <div className="w-1/5 lg:w-1/4 md:w-1/3 sm:w-1/2" key={item.id}>
                  <Link href="#" className="d-block">
                    <div className="text-15 fw-500">{item.city}</div>
                    <div className="text-14 text-light-1">
                      {item.properties} properties
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      {/* End .tabs__content */}
    </>
  );
};

export default Destinations;

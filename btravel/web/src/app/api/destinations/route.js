import { NextResponse } from 'next/server';

// Replace this with your actual backend API URL
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

export async function GET() {
  try {
    let rawData;
    
    // Try to fetch from the backend API first
    try {
      console.log(`Attempting to fetch destinations from: ${API_BASE_URL}/api/destinations/`);
      
      const controller = new AbortController();
      // Set a timeout to avoid long-hanging requests
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(`${API_BASE_URL}/api/destinations/`, {
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
        cache: 'no-store', // Don't cache the response
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`Backend API responded with status: ${response.status}`);
      }
      
      rawData = await response.json();
      console.log('Successfully fetched destinations from backend API');
      
      // Wrap the response in a data property
      return NextResponse.json({ data: rawData });
    } catch (fetchError) {
      console.error('Error fetching from backend API:', fetchError.message);
      // Re-throw to trigger the fallback
      throw fetchError;
    }
  } catch (error) {
    console.error('Failed to fetch destinations, using fallback data:', error.message);
    
    // Fallback data in case the API is not available
    const fallbackData = {
      data: [
        {
          id: '1',
          name: 'New York City',
          city: 'New York',
          country: 'USA',
          region: 'north_america',
          properties: 12,
          stays: Array(12).fill(null),
          img: '/img/destinations/1/1.png',
          hoverText: '12 Hotels - 7 Tours - 10 Activities'
        },
        {
          id: '2',
          name: 'London',
          city: 'London',
          country: 'UK',
          region: 'europe',
          properties: 14,
          stays: Array(14).fill(null),
          img: '/img/destinations/1/2.png',
          hoverText: '14 Hotels - 8 Tours - 12 Activities'
        },
        {
          id: '3',
          name: 'Paris',
          city: 'Paris',
          country: 'France',
          region: 'europe',
          properties: 16,
          stays: Array(16).fill(null),
          img: '/img/destinations/1/3.png',
          hoverText: '16 Hotels - 10 Tours - 15 Activities'
        },
        {
          id: '4',
          name: 'Tokyo',
          city: 'Tokyo',
          country: 'Japan',
          region: 'asia',
          properties: 15,
          stays: Array(15).fill(null),
          img: '/img/destinations/1/4.png',
          hoverText: '15 Hotels - 9 Tours - 12 Activities'
        },
        {
          id: '5',
          name: 'Rome',
          city: 'Rome',
          country: 'Italy',
          region: 'europe',
          properties: 10,
          stays: Array(10).fill(null),
          img: '/img/destinations/1/5.png',
          hoverText: '10 Hotels - 6 Tours - 8 Activities'
        },
        {
          id: '6',
          name: 'Barcelona',
          city: 'Barcelona',
          country: 'Spain',
          region: 'europe',
          properties: 8,
          stays: Array(8).fill(null),
          img: '/img/destinations/1/1.png',
          hoverText: '8 Hotels - 5 Tours - 7 Activities'
        },
        {
          id: '7',
          name: 'Dubai',
          city: 'Dubai',
          country: 'UAE',
          region: 'asia',
          properties: 17,
          stays: Array(17).fill(null),
          img: '/img/destinations/1/2.png',
          hoverText: '17 Hotels - 12 Tours - 18 Activities'
        },
        {
          id: '8',
          name: 'Bangkok',
          city: 'Bangkok',
          country: 'Thailand',
          region: 'asia',
          properties: 11,
          stays: Array(11).fill(null),
          img: '/img/destinations/1/3.png',
          hoverText: '11 Hotels - 7 Tours - 9 Activities'
        },
      ]
    };
    
    return NextResponse.json(fallbackData);
  }
} 
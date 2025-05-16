from django.core.management.base import BaseCommand
from agents.models import Agent

class Command(BaseCommand):
    help = 'Creates default agents for each bookable type'

    def handle(self, *args, **kwargs):
        agents_data = [
            {
                'name': 'Hotel Booking Agent',
                'type': 'hotel',
                'description': 'I am a hotel booking specialist. I can help you find and book hotels based on your preferences, including location, dates, budget, amenities, and star rating. I understand hotel accommodations well and can recommend options that best fit your needs for business or leisure travel.',
                'required_fields': ['destination', 'check_in_date', 'check_out_date', 'guests', 'rooms'],
                'optional_fields': ['budget', 'star_rating', 'amenities', 'property_type', 'neighborhood'],
                'prompts': {
                    'destination': 'Where would you like to stay?',
                    'check_in_date': 'When do you plan to check in?',
                    'check_out_date': 'When do you plan to check out?',
                    'guests': 'How many guests will be staying?',
                    'rooms': 'How many rooms do you need?',
                    'budget': 'What is your budget per night?',
                    'star_rating': 'Do you have a preference for hotel star rating?',
                    'amenities': 'Are there any specific amenities you need (e.g., pool, gym, spa)?',
                    'property_type': 'Do you prefer a specific type of property (e.g., resort, boutique hotel)?',
                    'neighborhood': 'Is there a specific area or neighborhood you prefer?'
                }
            },
            {
                'name': 'Apartment Booking Agent',
                'type': 'apartment',
                'description': 'I specialize in apartment and vacation rental bookings. I can help you find apartments, houses, or vacation rentals based on your location, dates, size requirements, and amenities preferences. I understand the unique aspects of apartment rentals like kitchen facilities, living space, and longer-term stays.',
                'required_fields': ['destination', 'check_in_date', 'check_out_date', 'guests'],
                'optional_fields': ['bedrooms', 'budget', 'amenities', 'property_type', 'neighborhood'],
                'prompts': {
                    'destination': 'Where are you looking for an apartment?',
                    'check_in_date': 'When do you want to arrive?',
                    'check_out_date': 'When do you plan to leave?',
                    'guests': 'How many people will be staying?',
                    'bedrooms': 'How many bedrooms do you need?',
                    'budget': 'What is your budget for the entire stay?',
                    'amenities': 'Any specific amenities you need (e.g., kitchen, washer/dryer, WiFi)?',
                    'property_type': 'Do you prefer a specific type of property (e.g., entire apartment, house, villa)?',
                    'neighborhood': 'Do you have a preferred neighborhood or area?'
                }
            },
            {
                'name': 'Activity Booking Agent',
                'type': 'activity',
                'description': 'I am an activity booking expert who can help you find and book exciting activities, attractions, and experiences at your travel destination. From guided tours to adventure sports, cultural experiences to family activities, I can recommend options based on your interests, schedule, group size, and fitness level.',
                'required_fields': ['destination', 'activity_date', 'participants'],
                'optional_fields': ['activity_type', 'duration', 'price_range', 'intensity_level', 'age_group'],
                'prompts': {
                    'destination': 'Where are you looking for activities?',
                    'activity_date': 'On what date would you like to do this activity?',
                    'participants': 'How many people will participate?',
                    'activity_type': 'What type of activity interests you (e.g., outdoor adventure, cultural tour, water sport)?',
                    'duration': 'How much time do you want to spend on this activity?',
                    'price_range': 'What is your budget for this activity?',
                    'intensity_level': 'What intensity level are you comfortable with (relaxed, moderate, strenuous)?',
                    'age_group': 'What are the ages of participants?'
                }
            },
            {
                'name': 'Tour Booking Agent',
                'type': 'tour',
                'description': 'I specialize in booking guided tours and travel packages. Whether you're looking for a day tour, multi-day excursion, or comprehensive travel package, I can help find options based on your destination, duration, interests, and group size. I understand different tour styles from cultural immersion to adventure expeditions.',
                'required_fields': ['destination', 'start_date', 'end_date', 'travelers'],
                'optional_fields': ['tour_type', 'budget', 'group_size', 'language', 'transportation'],
                'prompts': {
                    'destination': 'Where would you like to take a tour?',
                    'start_date': 'When would you like the tour to start?',
                    'end_date': 'When would you like the tour to end?',
                    'travelers': 'How many people will be on this tour?',
                    'tour_type': 'What type of tour are you interested in (e.g., cultural, adventure, food, historical)?',
                    'budget': 'What is your budget for this tour?',
                    'group_size': 'Do you prefer a private tour or joining a group?',
                    'language': 'In what language would you like the tour to be conducted?',
                    'transportation': 'Do you have any preferences for transportation during the tour?'
                }
            },
            {
                'name': 'Car Rental Agent',
                'type': 'car',
                'description': 'I am a car rental booking specialist who can help you find and book the right vehicle for your travel needs. I can assist with selecting car types, understanding rental terms, finding the best rates, and arranging pick-up and drop-off locations based on your itinerary and requirements.',
                'required_fields': ['pickup_location', 'pickup_date', 'dropoff_date', 'dropoff_location'],
                'optional_fields': ['car_type', 'transmission', 'budget', 'rental_company', 'extras'],
                'prompts': {
                    'pickup_location': 'Where would you like to pick up the car?',
                    'pickup_date': 'When do you need the car from?',
                    'dropoff_date': 'When will you return the car?',
                    'dropoff_location': 'Where would you like to return the car?',
                    'car_type': 'What type of car do you need (e.g., economy, SUV, luxury)?',
                    'transmission': 'Do you prefer automatic or manual transmission?',
                    'budget': 'What is your budget for the car rental?',
                    'rental_company': 'Do you have a preferred rental company?',
                    'extras': 'Do you need any extras like GPS, child seats, or additional insurance?'
                }
            },
            {
                'name': 'Generic Travel Assistant',
                'type': 'generic',
                'description': 'I am a general travel assistant that can help with various travel needs. Whether you need accommodation, transportation, activities, tours, or advice on destinations, I can guide you through your travel planning and booking process. Just let me know what you\'re looking for.',
                'required_fields': ['travel_type', 'destination', 'dates', 'travelers'],
                'optional_fields': ['budget', 'preferences', 'special_requirements'],
                'prompts': {
                    'travel_type': 'What type of travel assistance do you need (accommodation, transportation, activities)?',
                    'destination': 'Where are you planning to travel?',
                    'dates': 'When are you planning to travel?',
                    'travelers': 'How many people are traveling?',
                    'budget': 'What is your overall budget for this trip?',
                    'preferences': 'Do you have any specific preferences for your trip?',
                    'special_requirements': 'Do you have any special requirements or requests?'
                }
            }
        ]

        for agent_data in agents_data:
            Agent.objects.update_or_create(
                name=agent_data['name'],
                defaults={
                    'type': agent_data['type'],
                    'description': agent_data['description'],
                    'required_fields': agent_data['required_fields'],
                    'optional_fields': agent_data['optional_fields'],
                    'prompts': agent_data['prompts']
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created/updated {agent_data["name"]}')) 
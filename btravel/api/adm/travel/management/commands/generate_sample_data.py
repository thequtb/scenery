import random
from django.core.management.base import BaseCommand
from travel.models import Destination, Bookable, BookableImage
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample data for destinations and bookables'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating sample data...')
        
        # Create 10 destinations
        destinations = []
        destination_names = [
            "Paris, France",
            "Tokyo, Japan",
            "New York, USA",
            "Rome, Italy",
            "Sydney, Australia",
            "Barcelona, Spain",
            "London, UK",
            "Dubai, UAE",
            "Bali, Indonesia",
            "Cape Town, South Africa"
        ]
        
        self.stdout.write('Creating destinations...')
        for name in destination_names:
            destination, created = Destination.objects.get_or_create(name=name)
            destinations.append(destination)
            if created:
                self.stdout.write(f'Created destination: {name}')
            else:
                self.stdout.write(f'Destination already exists: {name}')
        
        # Create 100 bookables
        self.stdout.write('Creating bookables...')
        bookable_types = list(Bookable.BookableType.values)
        
        # Sample hotel names
        hotel_prefixes = ["Grand", "Royal", "Luxury", "Sunset", "Ocean", "Majestic", "Elite", "Premier", "Riverside", "Golden"]
        hotel_suffixes = ["Hotel", "Resort", "Suites", "Plaza", "Inn", "Lodge", "Retreat", "Palace", "Getaway", "Heights"]
        
        # Sample apartment names
        apartment_prefixes = ["Modern", "Urban", "Cozy", "Elegant", "City", "Downtown", "Skyline", "Central", "Deluxe", "Classic"]
        apartment_suffixes = ["Apartments", "Lofts", "Suites", "Residences", "Living", "Flats", "Studios", "Homes", "Quarters", "Villas"]
        
        # Sample activity names
        activity_prefixes = ["Guided", "Historic", "Adventure", "Cultural", "Local", "Scenic", "Exclusive", "Traditional", "Interactive", "Ultimate"]
        activity_suffixes = ["Tour", "Experience", "Adventure", "Workshop", "Class", "Excursion", "Activity", "Session", "Journey", "Discovery"]
        
        # Sample tour names
        tour_prefixes = ["Day", "Sunset", "Private", "Group", "Authentic", "Discovery", "Insider's", "Explorer's", "Guided", "Secret"]
        tour_suffixes = ["Tour", "Excursion", "Trip", "Adventure", "Experience", "Journey", "Expedition", "Exploration", "Visit", "Voyage"]
        
        # Sample car names
        car_prefixes = ["Luxury", "Economy", "Compact", "SUV", "Sports", "Convertible", "Electric", "Premium", "Classic", "Family"]
        car_suffixes = ["Car", "Vehicle", "Rental", "Auto", "Sedan", "Convertible", "Van", "SUV", "4x4", "Transport"]
        
        created_count = 0
        
        for i in range(100):
            # Select a random destination and bookable type
            destination = random.choice(destinations)
            bookable_type = random.choice(bookable_types)
            
            # Generate title based on type
            if bookable_type == 'hotel':
                title = f"{random.choice(hotel_prefixes)} {random.choice(hotel_suffixes)}"
            elif bookable_type == 'apartment':
                title = f"{random.choice(apartment_prefixes)} {random.choice(apartment_suffixes)}"
            elif bookable_type == 'activity':
                title = f"{random.choice(activity_prefixes)} {random.choice(activity_suffixes)}"
            elif bookable_type == 'tour':
                title = f"{random.choice(tour_prefixes)} {random.choice(tour_suffixes)}"
            elif bookable_type == 'car':
                title = f"{random.choice(car_prefixes)} {random.choice(car_suffixes)}"
            else:
                title = f"{fake.word().capitalize()} {fake.word().capitalize()}"
            
            # Make sure we don't create exact duplicates
            title = f"{title} {i+1}"
            
            # Generate options based on type
            options = {}
            
            if bookable_type == 'hotel':
                options = {
                    "description": fake.paragraph(),
                    "address": fake.address(),
                    "stars": random.randint(1, 5),
                    "amenities": random.sample([
                        "Wi-Fi", "Pool", "Gym", "Restaurant", "Bar", "Spa", 
                        "Room Service", "Parking", "Air Conditioning", "Breakfast Included"
                    ], k=random.randint(3, 8)),
                    "price_per_night": round(random.uniform(50, 500), 2),
                    "room_types": random.sample([
                        "Single", "Double", "Twin", "Suite", "Deluxe", "Executive"
                    ], k=random.randint(2, 5))
                }
            elif bookable_type == 'apartment':
                options = {
                    "description": fake.paragraph(),
                    "address": fake.address(),
                    "bedrooms": random.randint(1, 4),
                    "bathrooms": random.randint(1, 3),
                    "amenities": random.sample([
                        "Wi-Fi", "Kitchen", "Washing Machine", "TV", "Air Conditioning", 
                        "Heating", "Balcony", "Patio", "Parking", "Elevator"
                    ], k=random.randint(3, 8)),
                    "price_per_night": round(random.uniform(40, 400), 2),
                    "max_guests": random.randint(2, 8)
                }
            elif bookable_type == 'activity':
                options = {
                    "description": fake.paragraph(),
                    "duration": f"{random.randint(1, 5)} hours",
                    "price_per_person": round(random.uniform(20, 150), 2),
                    "included": random.sample([
                        "Guide", "Transportation", "Snacks", "Equipment", "Photos", 
                        "Drinks", "Insurance", "Admission Tickets"
                    ], k=random.randint(2, 6)),
                    "group_size": random.choice(["Small (1-5)", "Medium (6-15)", "Large (15+)"]),
                    "difficulty": random.choice(["Easy", "Moderate", "Challenging"])
                }
            elif bookable_type == 'tour':
                options = {
                    "description": fake.paragraph(),
                    "duration": f"{random.randint(1, 10)} hours",
                    "price_per_person": round(random.uniform(30, 200), 2),
                    "stops": [fake.street_name() for _ in range(random.randint(3, 8))],
                    "included": random.sample([
                        "Guide", "Transportation", "Lunch", "Dinner", "Snacks", 
                        "Drinks", "Admission Tickets", "Souvenir"
                    ], k=random.randint(3, 7)),
                    "languages": random.sample(["English", "Spanish", "French", "German", "Japanese", "Chinese"], k=random.randint(1, 3)),
                    "meeting_point": fake.street_address()
                }
            elif bookable_type == 'car':
                options = {
                    "description": fake.paragraph(),
                    "brand": random.choice(["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi", "Volvo", "Hyundai"]),
                    "model": fake.word().capitalize(),
                    "year": random.randint(2018, 2023),
                    "transmission": random.choice(["Automatic", "Manual"]),
                    "fuel_type": random.choice(["Gasoline", "Diesel", "Hybrid", "Electric"]),
                    "price_per_day": round(random.uniform(25, 300), 2),
                    "seats": random.randint(2, 7),
                    "features": random.sample([
                        "GPS", "Bluetooth", "Air Conditioning", "Cruise Control", 
                        "Backup Camera", "Sunroof", "Leather Seats", "Child Seat"
                    ], k=random.randint(3, 7))
                }
            else:
                options = {
                    "description": fake.paragraph(),
                    "price": round(random.uniform(20, 500), 2),
                    "features": [fake.word() for _ in range(random.randint(3, 8))]
                }
            
            # Create bookable
            bookable, created = Bookable.objects.get_or_create(
                title=title,
                destination=destination,
                type=bookable_type,
                defaults={'options': options}
            )
            
            if created:
                created_count += 1
                if created_count % 10 == 0:
                    self.stdout.write(f'Created {created_count} bookables...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new bookables for 10 destinations'))

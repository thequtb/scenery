# Script for populating the database. You can run it as:
#
#     mix run priv/repo/seeds.exs
#
# Inside the script, you can read and write to any of your
# repositories directly:
#
#     Api.Repo.insert!(%Api.SomeSchema{})
#
# We recommend using the bang functions (`insert!`, `update!`
# and so on) as they will fail if something goes wrong.

alias Api.Repo
alias Api.Accounts.User
alias Api.Accommodations.Stay
alias Api.Tours.Tour
alias Api.RentalCars.Car
alias Api.Bookings.Booking
alias Api.Destinations.Destination

# Create users
admin = Repo.insert!(%User{
  email: "admin@btravel.com",
  password_hash: Bcrypt.hash_pwd_salt("password123"),
  first_name: "Admin",
  last_name: "User",
  role: "admin"
})

customer = Repo.insert!(%User{
  email: "john@example.com",
  password_hash: Bcrypt.hash_pwd_salt("password123"),
  first_name: "John",
  last_name: "Doe",
  role: "customer"
})

# Create destinations
bali = Repo.insert!(%Destination{
  name: "Bali",
  description: "A beautiful island known for its beaches, temples, and vibrant culture",
  country: "Indonesia",
  city: "Denpasar",
  attractions: ["Ubud Monkey Forest", "Uluwatu Temple", "Tegallalang Rice Terraces", "Seminyak Beach"],
  image_urls: ["https://example.com/bali1.jpg", "https://example.com/bali2.jpg"],
  climate: "Tropical",
  best_time_to_visit: "April to October"
})

kyoto = Repo.insert!(%Destination{
  name: "Kyoto",
  description: "Historic city with beautiful temples, gardens, and traditional architecture",
  country: "Japan",
  city: "Kyoto",
  attractions: ["Fushimi Inari Shrine", "Kinkaku-ji", "Arashiyama Bamboo Grove", "Gion District"],
  image_urls: ["https://example.com/kyoto1.jpg", "https://example.com/kyoto2.jpg"],
  climate: "Temperate",
  best_time_to_visit: "March-May and October-November"
})

santorini = Repo.insert!(%Destination{
  name: "Santorini",
  description: "Stunning Greek island known for its white buildings and blue domes",
  country: "Greece",
  city: "Thira",
  attractions: ["Oia Sunset", "Fira", "Red Beach", "Ancient Akrotiri"],
  image_urls: ["https://example.com/santorini1.jpg", "https://example.com/santorini2.jpg"],
  climate: "Mediterranean",
  best_time_to_visit: "April to November"
})

# Create stays
stay1 = Repo.insert!(%Stay{
  name: "Luxury Beach Villa",
  description: "Beautiful beachfront villa with stunning ocean views",
  location: "Bali, Indonesia",
  price_per_night: Decimal.new("250.00"),
  amenities: ["Pool", "Wi-Fi", "Air conditioning", "Kitchen", "Beach access"],
  image_urls: ["https://example.com/villa1.jpg", "https://example.com/villa2.jpg"],
  max_guests: 6,
  destination_id: bali.id
})

stay2 = Repo.insert!(%Stay{
  name: "Mountain Cabin Retreat",
  description: "Cozy cabin in the mountains with fireplace",
  location: "Aspen, Colorado",
  price_per_night: Decimal.new("180.00"),
  amenities: ["Fireplace", "Wi-Fi", "Heating", "Kitchen", "Mountain view"],
  image_urls: ["https://example.com/cabin1.jpg", "https://example.com/cabin2.jpg"],
  max_guests: 4,
  destination_id: kyoto.id
})

# Create tours
tour1 = Repo.insert!(%Tour{
  name: "Ancient Temples Tour",
  description: "Explore ancient temples with a knowledgeable guide",
  location: "Siem Reap, Cambodia",
  price: Decimal.new("75.00"),
  duration_hours: Decimal.new("6.5"),
  image_urls: ["https://example.com/tour1.jpg", "https://example.com/tour2.jpg"],
  included_services: ["Guide", "Transportation", "Lunch", "Water"],
  destination_id: kyoto.id
})

tour2 = Repo.insert!(%Tour{
  name: "Wine Country Excursion",
  description: "Visit local wineries with tastings and lunch",
  location: "Napa Valley, USA",
  price: Decimal.new("120.00"),
  duration_hours: Decimal.new("8.0"),
  image_urls: ["https://example.com/wine1.jpg", "https://example.com/wine2.jpg"],
  included_services: ["Guide", "Transportation", "Wine tastings", "Lunch"],
  destination_id: santorini.id
})

# Create cars
car1 = Repo.insert!(%Car{
  model: "Corolla",
  make: "Toyota",
  year: 2022,
  price_per_day: Decimal.new("45.00"),
  seats: 5,
  transmission: "Automatic",
  fuel_type: "Gasoline",
  image_urls: ["https://example.com/corolla1.jpg", "https://example.com/corolla2.jpg"],
  available: true,
  destination_id: bali.id
})

car2 = Repo.insert!(%Car{
  model: "Model Y",
  make: "Tesla",
  year: 2023,
  price_per_day: Decimal.new("85.00"),
  seats: 5,
  transmission: "Automatic",
  fuel_type: "Electric",
  image_urls: ["https://example.com/tesla1.jpg", "https://example.com/tesla2.jpg"],
  available: true,
  destination_id: santorini.id
})

# Create bookings
Repo.insert!(%Booking{
  user_id: customer.id,
  stay_id: stay1.id,
  start_date: ~D[2023-07-15],
  end_date: ~D[2023-07-20],
  total_price: Decimal.new("1250.00"),
  status: "confirmed"
})

Repo.insert!(%Booking{
  user_id: customer.id,
  tour_id: tour1.id,
  start_date: ~D[2023-07-17],
  end_date: ~D[2023-07-17],
  total_price: Decimal.new("75.00"),
  status: "confirmed"
})

Repo.insert!(%Booking{
  user_id: customer.id,
  car_id: car2.id,
  start_date: ~D[2023-07-15],
  end_date: ~D[2023-07-20],
  total_price: Decimal.new("425.00"),
  status: "pending"
})

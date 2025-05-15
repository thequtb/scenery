defmodule Api.RentalCarsTest do
  use Api.DataCase

  alias Api.RentalCars

  describe "cars" do
    alias Api.RentalCars.Car

    import Api.RentalCarsFixtures

    @invalid_attrs %{year: nil, available: nil, make: nil, model: nil, price_per_day: nil, seats: nil, transmission: nil, fuel_type: nil, image_urls: nil}

    test "list_cars/0 returns all cars" do
      car = car_fixture()
      assert RentalCars.list_cars() == [car]
    end

    test "get_car!/1 returns the car with given id" do
      car = car_fixture()
      assert RentalCars.get_car!(car.id) == car
    end

    test "create_car/1 with valid data creates a car" do
      valid_attrs = %{year: 42, available: true, make: "some make", model: "some model", price_per_day: "120.5", seats: 42, transmission: "some transmission", fuel_type: "some fuel_type", image_urls: ["option1", "option2"]}

      assert {:ok, %Car{} = car} = RentalCars.create_car(valid_attrs)
      assert car.year == 42
      assert car.available == true
      assert car.make == "some make"
      assert car.model == "some model"
      assert car.price_per_day == Decimal.new("120.5")
      assert car.seats == 42
      assert car.transmission == "some transmission"
      assert car.fuel_type == "some fuel_type"
      assert car.image_urls == ["option1", "option2"]
    end

    test "create_car/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = RentalCars.create_car(@invalid_attrs)
    end

    test "update_car/2 with valid data updates the car" do
      car = car_fixture()
      update_attrs = %{year: 43, available: false, make: "some updated make", model: "some updated model", price_per_day: "456.7", seats: 43, transmission: "some updated transmission", fuel_type: "some updated fuel_type", image_urls: ["option1"]}

      assert {:ok, %Car{} = car} = RentalCars.update_car(car, update_attrs)
      assert car.year == 43
      assert car.available == false
      assert car.make == "some updated make"
      assert car.model == "some updated model"
      assert car.price_per_day == Decimal.new("456.7")
      assert car.seats == 43
      assert car.transmission == "some updated transmission"
      assert car.fuel_type == "some updated fuel_type"
      assert car.image_urls == ["option1"]
    end

    test "update_car/2 with invalid data returns error changeset" do
      car = car_fixture()
      assert {:error, %Ecto.Changeset{}} = RentalCars.update_car(car, @invalid_attrs)
      assert car == RentalCars.get_car!(car.id)
    end

    test "delete_car/1 deletes the car" do
      car = car_fixture()
      assert {:ok, %Car{}} = RentalCars.delete_car(car)
      assert_raise Ecto.NoResultsError, fn -> RentalCars.get_car!(car.id) end
    end

    test "change_car/1 returns a car changeset" do
      car = car_fixture()
      assert %Ecto.Changeset{} = RentalCars.change_car(car)
    end
  end
end

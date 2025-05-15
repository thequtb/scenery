defmodule Api.RentalCarsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.RentalCars` context.
  """

  @doc """
  Generate a car.
  """
  def car_fixture(attrs \\ %{}) do
    {:ok, car} =
      attrs
      |> Enum.into(%{
        available: true,
        fuel_type: "some fuel_type",
        image_urls: ["option1", "option2"],
        make: "some make",
        model: "some model",
        price_per_day: "120.5",
        seats: 42,
        transmission: "some transmission",
        year: 42
      })
      |> Api.RentalCars.create_car()

    car
  end
end

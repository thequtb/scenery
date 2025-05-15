defmodule Api.AccommodationsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.Accommodations` context.
  """

  @doc """
  Generate a stay.
  """
  def stay_fixture(attrs \\ %{}) do
    {:ok, stay} =
      attrs
      |> Enum.into(%{
        amenities: ["option1", "option2"],
        description: "some description",
        image_urls: ["option1", "option2"],
        location: "some location",
        max_guests: 42,
        name: "some name",
        price_per_night: "120.5"
      })
      |> Api.Accommodations.create_stay()

    stay
  end
end

defmodule Api.DestinationsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.Destinations` context.
  """

  @doc """
  Generate a destination.
  """
  def destination_fixture(attrs \\ %{}) do
    {:ok, destination} =
      attrs
      |> Enum.into(%{
        attractions: ["option1", "option2"],
        best_time_to_visit: "some best_time_to_visit",
        city: "some city",
        climate: "some climate",
        country: "some country",
        description: "some description",
        image_urls: ["option1", "option2"],
        name: "some name"
      })
      |> Api.Destinations.create_destination()

    destination
  end
end

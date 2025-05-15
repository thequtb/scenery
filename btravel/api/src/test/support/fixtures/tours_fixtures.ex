defmodule Api.ToursFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.Tours` context.
  """

  @doc """
  Generate a tour.
  """
  def tour_fixture(attrs \\ %{}) do
    {:ok, tour} =
      attrs
      |> Enum.into(%{
        description: "some description",
        duration_hours: "120.5",
        image_urls: ["option1", "option2"],
        included_services: ["option1", "option2"],
        location: "some location",
        name: "some name",
        price: "120.5"
      })
      |> Api.Tours.create_tour()

    tour
  end
end

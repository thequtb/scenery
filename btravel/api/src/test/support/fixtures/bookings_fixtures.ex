defmodule Api.BookingsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.Bookings` context.
  """

  @doc """
  Generate a booking.
  """
  def booking_fixture(attrs \\ %{}) do
    {:ok, booking} =
      attrs
      |> Enum.into(%{
        end_date: ~D[2025-05-14],
        start_date: ~D[2025-05-14],
        status: "some status",
        total_price: "120.5",
        user_id: "7488a646-e31f-11e4-aace-600308960662"
      })
      |> Api.Bookings.create_booking()

    booking
  end
end

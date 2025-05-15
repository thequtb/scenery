defmodule ApiWeb.BookingControllerTest do
  use ApiWeb.ConnCase

  import Api.BookingsFixtures

  alias Api.Bookings.Booking

  @create_attrs %{
    status: "some status",
    user_id: "7488a646-e31f-11e4-aace-600308960662",
    start_date: ~D[2025-05-14],
    end_date: ~D[2025-05-14],
    total_price: "120.5"
  }
  @update_attrs %{
    status: "some updated status",
    user_id: "7488a646-e31f-11e4-aace-600308960668",
    start_date: ~D[2025-05-15],
    end_date: ~D[2025-05-15],
    total_price: "456.7"
  }
  @invalid_attrs %{status: nil, user_id: nil, start_date: nil, end_date: nil, total_price: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all bookings", %{conn: conn} do
      conn = get(conn, ~p"/api/bookings")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create booking" do
    test "renders booking when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/bookings", booking: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/bookings/#{id}")

      assert %{
               "id" => ^id,
               "end_date" => "2025-05-14",
               "start_date" => "2025-05-14",
               "status" => "some status",
               "total_price" => "120.5",
               "user_id" => "7488a646-e31f-11e4-aace-600308960662"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/bookings", booking: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update booking" do
    setup [:create_booking]

    test "renders booking when data is valid", %{conn: conn, booking: %Booking{id: id} = booking} do
      conn = put(conn, ~p"/api/bookings/#{booking}", booking: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/bookings/#{id}")

      assert %{
               "id" => ^id,
               "end_date" => "2025-05-15",
               "start_date" => "2025-05-15",
               "status" => "some updated status",
               "total_price" => "456.7",
               "user_id" => "7488a646-e31f-11e4-aace-600308960668"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, booking: booking} do
      conn = put(conn, ~p"/api/bookings/#{booking}", booking: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete booking" do
    setup [:create_booking]

    test "deletes chosen booking", %{conn: conn, booking: booking} do
      conn = delete(conn, ~p"/api/bookings/#{booking}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/bookings/#{booking}")
      end
    end
  end

  defp create_booking(_) do
    booking = booking_fixture()
    %{booking: booking}
  end
end

defmodule ApiWeb.TourControllerTest do
  use ApiWeb.ConnCase

  import Api.ToursFixtures

  alias Api.Tours.Tour

  @create_attrs %{
    name: "some name",
    description: "some description",
    location: "some location",
    price: "120.5",
    duration_hours: "120.5",
    image_urls: ["option1", "option2"],
    included_services: ["option1", "option2"]
  }
  @update_attrs %{
    name: "some updated name",
    description: "some updated description",
    location: "some updated location",
    price: "456.7",
    duration_hours: "456.7",
    image_urls: ["option1"],
    included_services: ["option1"]
  }
  @invalid_attrs %{name: nil, description: nil, location: nil, price: nil, duration_hours: nil, image_urls: nil, included_services: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all tours", %{conn: conn} do
      conn = get(conn, ~p"/api/tours")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create tour" do
    test "renders tour when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/tours", tour: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/tours/#{id}")

      assert %{
               "id" => ^id,
               "description" => "some description",
               "duration_hours" => "120.5",
               "image_urls" => ["option1", "option2"],
               "included_services" => ["option1", "option2"],
               "location" => "some location",
               "name" => "some name",
               "price" => "120.5"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/tours", tour: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update tour" do
    setup [:create_tour]

    test "renders tour when data is valid", %{conn: conn, tour: %Tour{id: id} = tour} do
      conn = put(conn, ~p"/api/tours/#{tour}", tour: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/tours/#{id}")

      assert %{
               "id" => ^id,
               "description" => "some updated description",
               "duration_hours" => "456.7",
               "image_urls" => ["option1"],
               "included_services" => ["option1"],
               "location" => "some updated location",
               "name" => "some updated name",
               "price" => "456.7"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, tour: tour} do
      conn = put(conn, ~p"/api/tours/#{tour}", tour: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete tour" do
    setup [:create_tour]

    test "deletes chosen tour", %{conn: conn, tour: tour} do
      conn = delete(conn, ~p"/api/tours/#{tour}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/tours/#{tour}")
      end
    end
  end

  defp create_tour(_) do
    tour = tour_fixture()
    %{tour: tour}
  end
end

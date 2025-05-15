defmodule ApiWeb.CarControllerTest do
  use ApiWeb.ConnCase

  import Api.RentalCarsFixtures

  alias Api.RentalCars.Car

  @create_attrs %{
    year: 42,
    available: true,
    make: "some make",
    model: "some model",
    price_per_day: "120.5",
    seats: 42,
    transmission: "some transmission",
    fuel_type: "some fuel_type",
    image_urls: ["option1", "option2"]
  }
  @update_attrs %{
    year: 43,
    available: false,
    make: "some updated make",
    model: "some updated model",
    price_per_day: "456.7",
    seats: 43,
    transmission: "some updated transmission",
    fuel_type: "some updated fuel_type",
    image_urls: ["option1"]
  }
  @invalid_attrs %{year: nil, available: nil, make: nil, model: nil, price_per_day: nil, seats: nil, transmission: nil, fuel_type: nil, image_urls: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all cars", %{conn: conn} do
      conn = get(conn, ~p"/api/cars")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create car" do
    test "renders car when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/cars", car: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/cars/#{id}")

      assert %{
               "id" => ^id,
               "available" => true,
               "fuel_type" => "some fuel_type",
               "image_urls" => ["option1", "option2"],
               "make" => "some make",
               "model" => "some model",
               "price_per_day" => "120.5",
               "seats" => 42,
               "transmission" => "some transmission",
               "year" => 42
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/cars", car: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update car" do
    setup [:create_car]

    test "renders car when data is valid", %{conn: conn, car: %Car{id: id} = car} do
      conn = put(conn, ~p"/api/cars/#{car}", car: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/cars/#{id}")

      assert %{
               "id" => ^id,
               "available" => false,
               "fuel_type" => "some updated fuel_type",
               "image_urls" => ["option1"],
               "make" => "some updated make",
               "model" => "some updated model",
               "price_per_day" => "456.7",
               "seats" => 43,
               "transmission" => "some updated transmission",
               "year" => 43
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, car: car} do
      conn = put(conn, ~p"/api/cars/#{car}", car: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete car" do
    setup [:create_car]

    test "deletes chosen car", %{conn: conn, car: car} do
      conn = delete(conn, ~p"/api/cars/#{car}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/cars/#{car}")
      end
    end
  end

  defp create_car(_) do
    car = car_fixture()
    %{car: car}
  end
end

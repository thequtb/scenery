defmodule ApiWeb.DestinationControllerTest do
  use ApiWeb.ConnCase

  import Api.DestinationsFixtures

  alias Api.Destinations.Destination

  @create_attrs %{
    name: "some name",
    description: "some description",
    country: "some country",
    city: "some city",
    attractions: ["option1", "option2"],
    image_urls: ["option1", "option2"],
    climate: "some climate",
    best_time_to_visit: "some best_time_to_visit"
  }
  @update_attrs %{
    name: "some updated name",
    description: "some updated description",
    country: "some updated country",
    city: "some updated city",
    attractions: ["option1"],
    image_urls: ["option1"],
    climate: "some updated climate",
    best_time_to_visit: "some updated best_time_to_visit"
  }
  @invalid_attrs %{name: nil, description: nil, country: nil, city: nil, attractions: nil, image_urls: nil, climate: nil, best_time_to_visit: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all destinations", %{conn: conn} do
      conn = get(conn, ~p"/api/destinations")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create destination" do
    test "renders destination when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/destinations", destination: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/destinations/#{id}")

      assert %{
               "id" => ^id,
               "attractions" => ["option1", "option2"],
               "best_time_to_visit" => "some best_time_to_visit",
               "city" => "some city",
               "climate" => "some climate",
               "country" => "some country",
               "description" => "some description",
               "image_urls" => ["option1", "option2"],
               "name" => "some name"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/destinations", destination: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update destination" do
    setup [:create_destination]

    test "renders destination when data is valid", %{conn: conn, destination: %Destination{id: id} = destination} do
      conn = put(conn, ~p"/api/destinations/#{destination}", destination: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/destinations/#{id}")

      assert %{
               "id" => ^id,
               "attractions" => ["option1"],
               "best_time_to_visit" => "some updated best_time_to_visit",
               "city" => "some updated city",
               "climate" => "some updated climate",
               "country" => "some updated country",
               "description" => "some updated description",
               "image_urls" => ["option1"],
               "name" => "some updated name"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, destination: destination} do
      conn = put(conn, ~p"/api/destinations/#{destination}", destination: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete destination" do
    setup [:create_destination]

    test "deletes chosen destination", %{conn: conn, destination: destination} do
      conn = delete(conn, ~p"/api/destinations/#{destination}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/destinations/#{destination}")
      end
    end
  end

  defp create_destination(_) do
    destination = destination_fixture()
    %{destination: destination}
  end
end

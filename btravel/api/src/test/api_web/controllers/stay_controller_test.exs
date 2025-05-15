defmodule ApiWeb.StayControllerTest do
  use ApiWeb.ConnCase

  import Api.AccommodationsFixtures

  alias Api.Accommodations.Stay

  @create_attrs %{
    name: "some name",
    description: "some description",
    location: "some location",
    price_per_night: "120.5",
    amenities: ["option1", "option2"],
    image_urls: ["option1", "option2"],
    max_guests: 42
  }
  @update_attrs %{
    name: "some updated name",
    description: "some updated description",
    location: "some updated location",
    price_per_night: "456.7",
    amenities: ["option1"],
    image_urls: ["option1"],
    max_guests: 43
  }
  @invalid_attrs %{name: nil, description: nil, location: nil, price_per_night: nil, amenities: nil, image_urls: nil, max_guests: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all stays", %{conn: conn} do
      conn = get(conn, ~p"/api/stays")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create stay" do
    test "renders stay when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/stays", stay: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/stays/#{id}")

      assert %{
               "id" => ^id,
               "amenities" => ["option1", "option2"],
               "description" => "some description",
               "image_urls" => ["option1", "option2"],
               "location" => "some location",
               "max_guests" => 42,
               "name" => "some name",
               "price_per_night" => "120.5"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/stays", stay: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update stay" do
    setup [:create_stay]

    test "renders stay when data is valid", %{conn: conn, stay: %Stay{id: id} = stay} do
      conn = put(conn, ~p"/api/stays/#{stay}", stay: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/stays/#{id}")

      assert %{
               "id" => ^id,
               "amenities" => ["option1"],
               "description" => "some updated description",
               "image_urls" => ["option1"],
               "location" => "some updated location",
               "max_guests" => 43,
               "name" => "some updated name",
               "price_per_night" => "456.7"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, stay: stay} do
      conn = put(conn, ~p"/api/stays/#{stay}", stay: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete stay" do
    setup [:create_stay]

    test "deletes chosen stay", %{conn: conn, stay: stay} do
      conn = delete(conn, ~p"/api/stays/#{stay}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/stays/#{stay}")
      end
    end
  end

  defp create_stay(_) do
    stay = stay_fixture()
    %{stay: stay}
  end
end

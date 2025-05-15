defmodule Api.ToursTest do
  use Api.DataCase

  alias Api.Tours

  describe "tours" do
    alias Api.Tours.Tour

    import Api.ToursFixtures

    @invalid_attrs %{name: nil, description: nil, location: nil, price: nil, duration_hours: nil, image_urls: nil, included_services: nil}

    test "list_tours/0 returns all tours" do
      tour = tour_fixture()
      assert Tours.list_tours() == [tour]
    end

    test "get_tour!/1 returns the tour with given id" do
      tour = tour_fixture()
      assert Tours.get_tour!(tour.id) == tour
    end

    test "create_tour/1 with valid data creates a tour" do
      valid_attrs = %{name: "some name", description: "some description", location: "some location", price: "120.5", duration_hours: "120.5", image_urls: ["option1", "option2"], included_services: ["option1", "option2"]}

      assert {:ok, %Tour{} = tour} = Tours.create_tour(valid_attrs)
      assert tour.name == "some name"
      assert tour.description == "some description"
      assert tour.location == "some location"
      assert tour.price == Decimal.new("120.5")
      assert tour.duration_hours == Decimal.new("120.5")
      assert tour.image_urls == ["option1", "option2"]
      assert tour.included_services == ["option1", "option2"]
    end

    test "create_tour/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Tours.create_tour(@invalid_attrs)
    end

    test "update_tour/2 with valid data updates the tour" do
      tour = tour_fixture()
      update_attrs = %{name: "some updated name", description: "some updated description", location: "some updated location", price: "456.7", duration_hours: "456.7", image_urls: ["option1"], included_services: ["option1"]}

      assert {:ok, %Tour{} = tour} = Tours.update_tour(tour, update_attrs)
      assert tour.name == "some updated name"
      assert tour.description == "some updated description"
      assert tour.location == "some updated location"
      assert tour.price == Decimal.new("456.7")
      assert tour.duration_hours == Decimal.new("456.7")
      assert tour.image_urls == ["option1"]
      assert tour.included_services == ["option1"]
    end

    test "update_tour/2 with invalid data returns error changeset" do
      tour = tour_fixture()
      assert {:error, %Ecto.Changeset{}} = Tours.update_tour(tour, @invalid_attrs)
      assert tour == Tours.get_tour!(tour.id)
    end

    test "delete_tour/1 deletes the tour" do
      tour = tour_fixture()
      assert {:ok, %Tour{}} = Tours.delete_tour(tour)
      assert_raise Ecto.NoResultsError, fn -> Tours.get_tour!(tour.id) end
    end

    test "change_tour/1 returns a tour changeset" do
      tour = tour_fixture()
      assert %Ecto.Changeset{} = Tours.change_tour(tour)
    end
  end
end

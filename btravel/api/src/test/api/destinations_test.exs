defmodule Api.DestinationsTest do
  use Api.DataCase

  alias Api.Destinations

  describe "destinations" do
    alias Api.Destinations.Destination

    import Api.DestinationsFixtures

    @invalid_attrs %{name: nil, description: nil, country: nil, city: nil, attractions: nil, image_urls: nil, climate: nil, best_time_to_visit: nil}

    test "list_destinations/0 returns all destinations" do
      destination = destination_fixture()
      assert Destinations.list_destinations() == [destination]
    end

    test "get_destination!/1 returns the destination with given id" do
      destination = destination_fixture()
      assert Destinations.get_destination!(destination.id) == destination
    end

    test "create_destination/1 with valid data creates a destination" do
      valid_attrs = %{name: "some name", description: "some description", country: "some country", city: "some city", attractions: ["option1", "option2"], image_urls: ["option1", "option2"], climate: "some climate", best_time_to_visit: "some best_time_to_visit"}

      assert {:ok, %Destination{} = destination} = Destinations.create_destination(valid_attrs)
      assert destination.name == "some name"
      assert destination.description == "some description"
      assert destination.country == "some country"
      assert destination.city == "some city"
      assert destination.attractions == ["option1", "option2"]
      assert destination.image_urls == ["option1", "option2"]
      assert destination.climate == "some climate"
      assert destination.best_time_to_visit == "some best_time_to_visit"
    end

    test "create_destination/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Destinations.create_destination(@invalid_attrs)
    end

    test "update_destination/2 with valid data updates the destination" do
      destination = destination_fixture()
      update_attrs = %{name: "some updated name", description: "some updated description", country: "some updated country", city: "some updated city", attractions: ["option1"], image_urls: ["option1"], climate: "some updated climate", best_time_to_visit: "some updated best_time_to_visit"}

      assert {:ok, %Destination{} = destination} = Destinations.update_destination(destination, update_attrs)
      assert destination.name == "some updated name"
      assert destination.description == "some updated description"
      assert destination.country == "some updated country"
      assert destination.city == "some updated city"
      assert destination.attractions == ["option1"]
      assert destination.image_urls == ["option1"]
      assert destination.climate == "some updated climate"
      assert destination.best_time_to_visit == "some updated best_time_to_visit"
    end

    test "update_destination/2 with invalid data returns error changeset" do
      destination = destination_fixture()
      assert {:error, %Ecto.Changeset{}} = Destinations.update_destination(destination, @invalid_attrs)
      assert destination == Destinations.get_destination!(destination.id)
    end

    test "delete_destination/1 deletes the destination" do
      destination = destination_fixture()
      assert {:ok, %Destination{}} = Destinations.delete_destination(destination)
      assert_raise Ecto.NoResultsError, fn -> Destinations.get_destination!(destination.id) end
    end

    test "change_destination/1 returns a destination changeset" do
      destination = destination_fixture()
      assert %Ecto.Changeset{} = Destinations.change_destination(destination)
    end
  end
end

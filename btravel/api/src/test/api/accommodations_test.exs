defmodule Api.AccommodationsTest do
  use Api.DataCase

  alias Api.Accommodations

  describe "stays" do
    alias Api.Accommodations.Stay

    import Api.AccommodationsFixtures

    @invalid_attrs %{name: nil, description: nil, location: nil, price_per_night: nil, amenities: nil, image_urls: nil, max_guests: nil}

    test "list_stays/0 returns all stays" do
      stay = stay_fixture()
      assert Accommodations.list_stays() == [stay]
    end

    test "get_stay!/1 returns the stay with given id" do
      stay = stay_fixture()
      assert Accommodations.get_stay!(stay.id) == stay
    end

    test "create_stay/1 with valid data creates a stay" do
      valid_attrs = %{name: "some name", description: "some description", location: "some location", price_per_night: "120.5", amenities: ["option1", "option2"], image_urls: ["option1", "option2"], max_guests: 42}

      assert {:ok, %Stay{} = stay} = Accommodations.create_stay(valid_attrs)
      assert stay.name == "some name"
      assert stay.description == "some description"
      assert stay.location == "some location"
      assert stay.price_per_night == Decimal.new("120.5")
      assert stay.amenities == ["option1", "option2"]
      assert stay.image_urls == ["option1", "option2"]
      assert stay.max_guests == 42
    end

    test "create_stay/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Accommodations.create_stay(@invalid_attrs)
    end

    test "update_stay/2 with valid data updates the stay" do
      stay = stay_fixture()
      update_attrs = %{name: "some updated name", description: "some updated description", location: "some updated location", price_per_night: "456.7", amenities: ["option1"], image_urls: ["option1"], max_guests: 43}

      assert {:ok, %Stay{} = stay} = Accommodations.update_stay(stay, update_attrs)
      assert stay.name == "some updated name"
      assert stay.description == "some updated description"
      assert stay.location == "some updated location"
      assert stay.price_per_night == Decimal.new("456.7")
      assert stay.amenities == ["option1"]
      assert stay.image_urls == ["option1"]
      assert stay.max_guests == 43
    end

    test "update_stay/2 with invalid data returns error changeset" do
      stay = stay_fixture()
      assert {:error, %Ecto.Changeset{}} = Accommodations.update_stay(stay, @invalid_attrs)
      assert stay == Accommodations.get_stay!(stay.id)
    end

    test "delete_stay/1 deletes the stay" do
      stay = stay_fixture()
      assert {:ok, %Stay{}} = Accommodations.delete_stay(stay)
      assert_raise Ecto.NoResultsError, fn -> Accommodations.get_stay!(stay.id) end
    end

    test "change_stay/1 returns a stay changeset" do
      stay = stay_fixture()
      assert %Ecto.Changeset{} = Accommodations.change_stay(stay)
    end
  end
end

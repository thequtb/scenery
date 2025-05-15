defmodule Api.Repo.Migrations.CreateStays do
  use Ecto.Migration

  def change do
    create table(:stays, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :name, :string
      add :description, :text
      add :location, :string
      add :price_per_night, :decimal
      add :amenities, {:array, :string}
      add :image_urls, {:array, :string}
      add :max_guests, :integer

      timestamps(type: :utc_datetime)
    end
  end
end

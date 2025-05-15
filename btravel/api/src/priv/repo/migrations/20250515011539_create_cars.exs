defmodule Api.Repo.Migrations.CreateCars do
  use Ecto.Migration

  def change do
    create table(:cars, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :model, :string
      add :make, :string
      add :year, :integer
      add :price_per_day, :decimal
      add :seats, :integer
      add :transmission, :string
      add :fuel_type, :string
      add :image_urls, {:array, :string}
      add :available, :boolean, default: false, null: false

      timestamps(type: :utc_datetime)
    end
  end
end

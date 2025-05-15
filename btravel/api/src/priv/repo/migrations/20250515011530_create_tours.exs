defmodule Api.Repo.Migrations.CreateTours do
  use Ecto.Migration

  def change do
    create table(:tours, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :name, :string
      add :description, :text
      add :location, :string
      add :price, :decimal
      add :duration_hours, :decimal
      add :image_urls, {:array, :string}
      add :included_services, {:array, :string}

      timestamps(type: :utc_datetime)
    end
  end
end

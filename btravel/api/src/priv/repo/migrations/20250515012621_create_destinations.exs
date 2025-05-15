defmodule Api.Repo.Migrations.CreateDestinations do
  use Ecto.Migration

  def change do
    create table(:destinations, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :name, :string
      add :description, :text
      add :country, :string
      add :city, :string
      add :attractions, {:array, :string}
      add :image_urls, {:array, :string}
      add :climate, :string
      add :best_time_to_visit, :string

      timestamps(type: :utc_datetime)
    end
  end
end

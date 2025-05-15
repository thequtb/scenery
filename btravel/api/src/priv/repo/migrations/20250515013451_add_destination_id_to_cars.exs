defmodule Api.Repo.Migrations.AddDestinationIdToCars do
  use Ecto.Migration

  def change do
    alter table(:cars) do
      add :destination_id, references(:destinations, type: :binary_id, on_delete: :nothing)
    end

    create index(:cars, [:destination_id])
  end
end

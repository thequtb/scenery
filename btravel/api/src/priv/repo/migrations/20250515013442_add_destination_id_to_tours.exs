defmodule Api.Repo.Migrations.AddDestinationIdToTours do
  use Ecto.Migration

  def change do
    alter table(:tours) do
      add :destination_id, references(:destinations, type: :binary_id, on_delete: :nothing)
    end

    create index(:tours, [:destination_id])
  end
end

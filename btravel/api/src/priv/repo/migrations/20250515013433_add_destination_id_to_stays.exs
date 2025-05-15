defmodule Api.Repo.Migrations.AddDestinationIdToStays do
  use Ecto.Migration

  def change do
    alter table(:stays) do
      add :destination_id, references(:destinations, type: :binary_id, on_delete: :nothing)
    end

    create index(:stays, [:destination_id])
  end
end

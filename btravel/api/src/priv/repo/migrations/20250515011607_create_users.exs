defmodule Api.Repo.Migrations.CreateUsers do
  use Ecto.Migration

  def change do
    create table(:users, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :email, :string
      add :password_hash, :string
      add :first_name, :string
      add :last_name, :string
      add :role, :string

      timestamps(type: :utc_datetime)
    end
  end
end

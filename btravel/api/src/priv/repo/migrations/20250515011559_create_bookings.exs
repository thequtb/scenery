defmodule Api.Repo.Migrations.CreateBookings do
  use Ecto.Migration

  def change do
    create table(:bookings, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :user_id, :uuid
      add :start_date, :date
      add :end_date, :date
      add :total_price, :decimal
      add :status, :string
      add :stay_id, references(:stays, on_delete: :nothing, type: :binary_id)
      add :tour_id, references(:tours, on_delete: :nothing, type: :binary_id)
      add :car_id, references(:cars, on_delete: :nothing, type: :binary_id)

      timestamps(type: :utc_datetime)
    end

    create index(:bookings, [:stay_id])
    create index(:bookings, [:tour_id])
    create index(:bookings, [:car_id])
  end
end

defmodule Journal.Repo.Migrations.CreateTelegramMessages do
  use Ecto.Migration

  def change do
    create table(:telegram_messages) do
      add :message_id, :string, null: false
      add :chat_id, :string
      add :text, :text
      add :json_data, :map, null: false
      add :processed_at, :utc_datetime
      add :tg_notified, :boolean, default: false
      add :notification_sent_at, :utc_datetime

      timestamps()
    end

    create index(:telegram_messages, [:message_id])
    create index(:telegram_messages, [:tg_notified])
  end
end 
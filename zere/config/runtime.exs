import Config
import Dotenvy

env_dir_prefix = System.get_env("RELEASE_ROOT") || Path.expand("./envs")

source!([
  Path.absname(".env", env_dir_prefix),
  Path.absname(".#{config_env()}.env", env_dir_prefix),
  System.get_env()
])


config :zere, Zere.Repo,
  database: env!("DB_NAME"),
  username: env!("DB_USER"),
  password: env!("DB_PASSWORD"),
  hostname: env!("DB_HOST"),
  port: env!("DB_PORT")

config :zere, ZereWeb.Endpoint,
  http: [
    ip: {127, 0, 0, 1},
    port: env!("PORT")
  ]
  

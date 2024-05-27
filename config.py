from pathlib import Path

from dotenv import load_dotenv, dotenv_values


root = Path(".").resolve()


env = dotenv_values()
load_dotenv()


db_user, db_password, db_host, db_port, db_name = db_params = tuple(
    env.get(param_name) for param_name in ["db_user", "db_password", "db_host", "db_port", "db_name"]
)


db_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(*db_params)

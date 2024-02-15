# global configs

from dotenv import load_dotenv
import os
from pydantic_settings  import BaseSettings

dotenv_path_1 = "./.env"
load_dotenv(dotenv_path_1, override=True)

# database
class DB_Settings(BaseSettings):
    print(os.getenv("DB_DB"))
    print(os.getenv("DB_DB"))
    print(os.getenv("DB_DB"))
    print(os.getenv("DB_DB"))
    print(os.getenv("DB_DB"))
    db_db: str = os.getenv("DB_DB")
    db_host: str = os.getenv("DB_HOST")
    db_password: str = os.getenv("DB_PASSWORD")
    db_port: int = int(os.getenv("DB_PORT"))
    db_user: str = os.getenv("DB_USER")

class OPENAI_Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
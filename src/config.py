# global configs

from dotenv import load_dotenv
import os
from pydantic_settings  import BaseSettings

dotenv_path_1 = "../.env"
dotenv_path_2 = ".env"
load_dotenv(dotenv_path_1)
load_dotenv(dotenv_path_2)

# SSH settings
class SSH_Settings(BaseSettings):
    ssh_host: str = os.getenv("SSH_HOST")
    ssh_port : int = int(os.getenv("SSH_PORT"))
    ssh_user : str = os.getenv("SSH_USER")
    ssh_pem : str = os.getenv("SSH_PEM")

# database
class DB_Settings(BaseSettings):
    db_address: str = os.getenv("DB_ADDRESS")
    db_port: int = int(os.getenv("DB_PORT"))
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_name: str = os.getenv("DB_NAME")
    
class OPENAI_Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
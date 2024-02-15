from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, declarative_base
from sqlalchemy.orm import sessionmaker

from config import SSH_Settings, DB_Settings

ssh_settings = SSH_Settings()
db_settings = DB_Settings()

# SSH 및 데이터베이스 접속 설정
SSH_HOST = ssh_settings.ssh_host
SSH_PORT = ssh_settings.ssh_port
SSH_USERNAME = ssh_settings.ssh_user
SSH_PEM = ssh_settings.ssh_pem
REMOTE_DATABASE_ADDRESS = db_settings.db_address
REMOTE_DATABASE_PORT = db_settings.db_port
DB_USER = db_settings.db_user
DB_PASSWORD = db_settings.db_password
DB_NAME = db_settings.db_name

# SQLAlchemy Base 클래스 정의
Base = declarative_base()

# SSH 터널을 사용하여 데이터베이스 엔진 및 세션 생성
with SSHTunnelForwarder(
    (SSH_HOST, SSH_PORT),
    ssh_username=SSH_USERNAME,
    ssh_private_key=SSH_PEM,
    # ssh_private_key_password='your_private_key_passphrase',  # 필요한 경우 주석 해제
    remote_bind_address=(REMOTE_DATABASE_ADDRESS, REMOTE_DATABASE_PORT)
) as tunnel:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:{tunnel.local_bind_port}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

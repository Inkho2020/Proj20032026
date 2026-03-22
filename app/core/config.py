from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

# BASE_DIR = Path(__file__).parent.parent.parent

DB_PATH = f"postgres:1234@localhost:5432/proj2"


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_PATH}"
    # db_host: str = f"sqlite+aiosqlite:///{(BASE_DIR / 'proj2.db').as_posix()}"
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"  # prefix for api_v1

    db: DbSettings = DbSettings()
    # db_url: str = f"postgresql+asyncpg://postgres:1234@localhost:5432/proj2"
    # # db_host: str = f"sqlite+aiosqlite:///{(BASE_DIR / 'proj2.db').as_posix()}"
    # db_echo: bool = True
    # db_port: int
    # db_name: str
    # db_name: str
    # db_password: str
    # db_user: str


settings = Settings()

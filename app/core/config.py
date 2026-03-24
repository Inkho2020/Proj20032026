from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent
PRIVATE_KEY = BASE_DIR / "certs" / "jwt-private.pem"
PUBLIC_KEY = BASE_DIR / "certs" / "jwt-public.pem"
DB_PATH = f"postgres:1234@localhost:5432/proj2"


class AuthJWT(BaseModel):
    private_key_path: str = PRIVATE_KEY
    public_key_path: str = PUBLIC_KEY
    algorithm: str = 'RS256'
    access_token_expire_min: int = 15
    refresh_token_expire_time: int = 30


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_PATH}"
    # db_host: str = f"sqlite+aiosqlite:///{(BASE_DIR / 'proj2.db').as_posix()}"
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"  # prefix for api_v1

    db: DbSettings = DbSettings()

    authJWT: AuthJWT = AuthJWT()

    # db_url: str = f"postgresql+asyncpg://postgres:1234@localhost:5432/proj2"
    # # db_host: str = f"sqlite+aiosqlite:///{(BASE_DIR / 'proj2.db').as_posix()}"
    # db_echo: bool = True
    # db_port: int
    # db_name: str
    # db_name: str
    # db_password: str
    # db_user: str


settings = Settings()

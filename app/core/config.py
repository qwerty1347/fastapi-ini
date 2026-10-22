from typing import Literal
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "fastapi-starter API"
    API_PREFIX: str = "/api"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # 브라우저에서 이 API 를 직접 호출하는 프론트 주소 (CORS 허용)
    FRONTEND_HOST: str = "http://localhost:3001"

    # 업무 기준 시간대 ('오늘 0시', 화면에 보여줄 시각). DB 저장도 이 시간대(KST)로 한다. → core/clock.py
    TIMEZONE: str = "Asia/Seoul"

    # 비동기 드라이버(aiomysql) 주소. 로컬은 .env, 도커는 compose 가 컨테이너용 주소로 덮어쓴다
    DATABASE_URL: str

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE)

    @property
    def database_url_sync(self) -> str:
        """동기 드라이버(pymysql) 주소. 접속 정보는 DATABASE_URL 하나로 관리하고 드라이버 이름만 바꾼다."""
        url = make_url(self.DATABASE_URL).set(drivername="mysql+pymysql")
        return url.render_as_string(hide_password=False)


settings = Settings()

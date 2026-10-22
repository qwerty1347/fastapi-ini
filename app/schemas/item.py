"""예제 스키마. 요청(Create)과 응답(Public)을 나눈다."""

from pydantic import AwareDatetime, ConfigDict, Field

from app.schemas.common import CamelModel


class ItemCreate(CamelModel):
    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)


class ItemPublic(CamelModel):
    # ORM 객체(app.models.Item)를 바로 model_validate 할 수 있게 한다
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    created_at: AwareDatetime
    """타임존 포함 시각. JSON: 2026-10-22T15:34:00+09:00"""

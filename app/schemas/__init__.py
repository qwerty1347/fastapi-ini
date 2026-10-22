"""API 요청·응답 스키마 (Pydantic). DB 테이블 모델은 app/models/ 에 둔다.

도메인별 파일로 나누고, 여기서 다시 내보내 `from app.schemas import ItemPublic` 처럼 쓴다.
"""

from app.schemas.common import ApiError, ApiResponse, CamelModel, FieldError
from app.schemas.item import ItemCreate, ItemPublic

__all__ = [
    "ApiError",
    "ApiResponse",
    "CamelModel",
    "FieldError",
    "ItemCreate",
    "ItemPublic",
]

"""DB 테이블 모델. API 응답 모양(app/schemas/)과는 따로 둔다.

여기서 모든 모델을 import 해야 Alembic --autogenerate 가 테이블을 빠짐없이 찾는다.
"""

from app.models.item import Item

__all__ = ["Item"]

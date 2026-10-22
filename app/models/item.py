"""예제 모델. 새 테이블은 이 모양을 복사해서 만들고 models/__init__.py 에 추가한다."""

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core import clock
from app.core.db import Base, KSTDateTime


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(KSTDateTime, default=clock.now)

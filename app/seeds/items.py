"""예제 시드. 기준 시각 now 를 받아 상대 날짜로 넣는다 (테스트에서는 고정 시각을 넣는다)."""

from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models import Item

ITEMS = [
    ("오버핏 코튼 셔츠", 39_000),
    ("무선 이어폰", 89_000),
    ("수분 크림", 24_500),
]


def seed(session: Session, now: datetime) -> None:
    session.execute(delete(Item))
    session.add_all(
        Item(name=name, price=price, created_at=now - timedelta(days=i))
        for i, (name, price) in enumerate(ITEMS)
    )
    session.flush()

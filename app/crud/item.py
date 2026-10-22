"""items 테이블 조회·저장. 쿼리만 하고 commit 은 하지 않는다 (services 가 한다)."""

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item


async def get(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


async def list_page(session: AsyncSession, offset: int, limit: int) -> Sequence[Item]:
    """최신순"""
    rows = await session.scalars(
        select(Item).order_by(Item.id.desc()).offset(offset).limit(limit)
    )
    return rows.all()


async def count(session: AsyncSession) -> int:
    total = await session.scalar(select(func.count()).select_from(Item))
    return total or 0


async def create(session: AsyncSession, name: str, price: int) -> Item:
    item = Item(name=name, price=price)
    session.add(item)
    await session.flush()  # INSERT 해서 id 를 받는다
    # DB 에 저장된 값으로 다시 읽는다. DATETIME 은 초 단위라 메모리의 마이크로초와 달라지기 때문
    await session.refresh(item)
    return item

"""예제 서비스. crud 를 부르고 응답 스키마로 바꾼다. 없는 데이터는 AppError 로 던진다."""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.crud import item as item_crud
from app.schemas import ItemCreate, ItemPublic


async def list_items(
    session: AsyncSession, offset: int, limit: int
) -> tuple[list[ItemPublic], int]:
    """(현재 페이지, 전체 개수)"""
    items = await item_crud.list_page(session, offset, limit)
    total = await item_crud.count(session)
    return [ItemPublic.model_validate(item) for item in items], total


async def get_item(session: AsyncSession, item_id: int) -> ItemPublic:
    item = await item_crud.get(session, item_id)
    if item is None:
        raise AppError(
            status.HTTP_404_NOT_FOUND, "ITEM_NOT_FOUND", "상품을 찾을 수 없어요"
        )
    return ItemPublic.model_validate(item)


async def create_item(session: AsyncSession, data: ItemCreate) -> ItemPublic:
    item = await item_crud.create(session, name=data.name, price=data.price)
    await session.commit()
    return ItemPublic.model_validate(item)

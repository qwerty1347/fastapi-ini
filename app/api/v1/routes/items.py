"""예제 라우트. 라우트는 요청을 받고 services 를 부르기만 한다 (쿼리·계산은 services/crud)."""

from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.api.deps import AsyncSessionDep
from app.core.errors import error_responses
from app.schemas import ApiResponse, ItemCreate, ItemPublic
from app.services import item as item_service

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", responses=error_responses(status.HTTP_422_UNPROCESSABLE_CONTENT))
async def read_items(
    session: AsyncSessionDep,
    response: Response,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ApiResponse[list[ItemPublic]]:
    items, total = await item_service.list_items(session, offset, limit)
    # 전체 개수는 헤더로 내려준다 (본문 모양은 다른 API 와 같게 유지)
    response.headers["X-Total-Count"] = str(total)
    return ApiResponse(data=items)


@router.get(
    "/{item_id}",
    responses=error_responses(
        status.HTTP_404_NOT_FOUND, status.HTTP_422_UNPROCESSABLE_CONTENT
    ),
)
async def read_item(session: AsyncSessionDep, item_id: int) -> ApiResponse[ItemPublic]:
    return ApiResponse(data=await item_service.get_item(session, item_id))


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=error_responses(status.HTTP_422_UNPROCESSABLE_CONTENT),
)
async def create_item(
    session: AsyncSessionDep, data: ItemCreate
) -> ApiResponse[ItemPublic]:
    item = await item_service.create_item(session, data)
    return ApiResponse(status_code=status.HTTP_201_CREATED, data=item)

from fastapi import APIRouter

from app.api.v1.routes import items, utils

router = APIRouter(prefix="/v1")
router.include_router(utils.router)
router.include_router(items.router)

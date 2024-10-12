from fastapi import APIRouter
from users.routers.v1.users import router as users_router
from auth.routers.auth_router import router as auth_router
router = APIRouter()

router.include_router(users_router)
router.include_router(auth_router)

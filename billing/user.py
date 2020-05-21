from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserOut(BaseModel):
    """Basic user fields."""

    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserOut):
    """Inherits UserOut and add write only password as an example."""

    password: str


@router.post("/", response_model=UserOut)
async def create_user(*, user: UserIn):
    """Create user in db."""
    return user

from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from billing import models
from billing.database import get_db

router = APIRouter()


class UserOut(BaseModel):
    """Basic user fields."""

    username: str
    email: EmailStr
    full_name: Optional[str] = None
    balance: int


class UserIn(UserOut):
    """Inherits UserOut and add write only password as an example."""

    password: str


@router.post("/", response_model=UserOut)
async def create_user(*, user: UserIn, db: Session = Depends(get_db)):
    """Create user in db."""
    user_dict = user.dict()
    user_dict.pop("password")  # don't save password in db
    # balance = user_dict.pop("balance") TODO: not implemented yet
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

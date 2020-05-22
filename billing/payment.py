from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from billing import models
from billing.database import get_db
from billing.models import NotEnoughFounds

router = APIRouter()


class Payment(BaseModel):
    """Simple payment."""

    debit_id: int
    credit_id: int
    amount: int


@router.post("/", response_model=Payment)
async def create_payment(*, payment: Payment, db: Session = Depends(get_db)):
    """Create payment transaction."""
    db_payment = models.Payment(**payment.dict())
    credit_user = db.query(models.User).get(db_payment.credit_id)
    debit_user = db.query(models.User).get(db_payment.debit_id)
    db.add(db_payment)
    try:
        credit_user.last_payment = db_payment
        debit_user.last_payment = db_payment
        db.add(credit_user)
        db.add(debit_user)
        db.commit()
        return payment
    except NotEnoughFounds:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="not enough founds"
        )

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    column,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from billing.database import Base


class NotEnoughFounds(Exception):
    """Occurs when not enough founds on wallet."""


class User(Base):
    """User and Wallet model."""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, unique=True, nullable=True)
    balance = Column(
        Integer, doc="wallet balance in USD cents, so 12345 == $123.45", nullable=False
    )
    CheckConstraint(column("balance") >= 0)  # balance cannot be negative
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    version_id = Column(
        Integer,
        nullable=False,
        doc="that field prevent concurrent write / race condition",
        default=0,
        # more info: https://docs.sqlalchemy.org/en/13/orm/versioning.html#simple-version-counting
    )
    last_payment_id = Column(Integer, ForeignKey("payment.id", ondelete="CASCADE"))
    last_payment = relationship(
        "Payment", foreign_keys=[last_payment_id], post_update=True
    )

    # __mapper_args__ = {"version_id_col": version_id}

    @validates("last_payment")
    def update_balance(self, key, value):
        """Main payment logic to check available amount."""
        if value.debit == self or (self.id is not None and value.debit_id == self.id):
            self.balance += value.amount
        elif value.credit == self or (
            self.id is not None and value.credit_id == self.id
        ):
            self.balance -= value.amount
        else:
            raise Exception("Should never occurs")
        if self.balance < 0:
            raise NotEnoughFounds()
        return value


class Payment(Base):
    """Payment transaction between Wallets."""

    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, doc="Value in USD cents, so 12345 == $123.45")
    created = Column(DateTime(timezone=True), server_default=func.now())
    credit_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        doc="is Null when admin adds initial founds into system",
    )
    credit = relationship("User", foreign_keys=[credit_id])
    debit_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    debit = relationship("User", foreign_keys=[debit_id])

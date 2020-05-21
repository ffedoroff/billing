from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    FetchedValue,
    ForeignKey,
    Integer,
    String,
    column,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from billing.database import Base


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
    xmin = Column(
        "xmin",
        Integer,
        system=True,
        server_default=FetchedValue(),
        doc="that field prevent concurrent write / race condition",
        # more info: https://docs.sqlalchemy.org/en/13/orm/versioning.html#server-side-version-counters
    )
    __mapper_args__ = {"version_id_col": xmin, "version_id_generator": False}
    last_payment_id = Column(Integer, ForeignKey("payment.id"), nullable=True)
    last_payment = relationship("Payment", foreign_keys=[last_payment_id])


class Payment(Base):
    """Payment transaction between Wallets."""

    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, doc="Value in USD cents, so 12345 == $123.45")
    created = Column(DateTime(timezone=True), server_default=func.now())
    credit_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=True,
        doc="is Null when admin adds initial founds into system",
    )
    credit = relationship("User", foreign_keys=[credit_id])
    debit_id = Column(Integer, ForeignKey("user.id"))
    debit = relationship("User", foreign_keys=[debit_id])

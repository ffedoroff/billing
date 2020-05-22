from fastapi import FastAPI

from billing import payment, user
from billing.database import Base, engine

app = FastAPI()

app.include_router(
    user.router, prefix="/users", tags=["users"],
)
app.include_router(
    payment.router, prefix="/payments", tags=["payments"],
)

Base.metadata.create_all(bind=engine)

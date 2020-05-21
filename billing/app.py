from fastapi import FastAPI

from billing import user
from billing.database import Base, engine

app = FastAPI()

app.include_router(
    user.router, prefix="/users", tags=["users"],
)

Base.metadata.create_all(bind=engine)

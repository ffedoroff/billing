import asyncio

from billing import models
from billing.database import get_db
from billing.user import UserIn, create_user

if __name__ == "__main__":
    # cleanup all users and payments
    db = next(get_db())
    db.query(models.Payment).delete()
    db.query(models.User).delete()
    db.commit()

    # create sample users for concurrent write tests
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            create_user(
                user=UserIn(
                    username=i, balance=10, email=f"{i}@bar.com", full_name=i, password=i,
                ),
                db=db,
            )
        )
        for i in range(10)
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

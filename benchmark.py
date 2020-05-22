import asyncio
import random

from billing import models
from billing.database import get_db
from billing.payment import Payment, create_payment

db = next(get_db())
user_ids = {user.id for user in db.query(models.User)}
loop = asyncio.get_event_loop()

# create many transactions
for i in range(100):
    tasks = []
    db = next(get_db())
    for chunk in range(200):
        debit_id, credit_id = random.sample(user_ids, 2)
        tasks.append(
            loop.create_task(
                create_payment(
                    payment=Payment(debit_id=debit_id, credit_id=credit_id, amount=2),
                    db=db,
                )
            )
        )
    loop.run_until_complete(asyncio.wait(tasks))

loop.close()

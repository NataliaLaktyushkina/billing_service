import secrets
import string
import uuid
from datetime import datetime
from typing import List, Optional

from werkzeug.security import generate_password_hash

from database.db import Base, SessionLocal
from database.db_models import User, PaymentsNew


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()
    return user


def generate_password():

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    return password


def create_user(username, email, password:Optional[str] = None):
    if password is None:
        password = generate_password()
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(login=username,
                    password=hashed_password,
                    email=email)
    service = SessionLocal()
    service.add(new_user)
    service.commit()

    return new_user


async def add_payment(payment_data: List[dict]):
    service = SessionLocal()
    for payment in payment_data:
        new_payment = PaymentsNew(
                    user_id=payment["user_id"],
                    payment_id=payment["payment_id"],
                    payment_date=payment["payment_date"],
                    payment_type=payment["payment_type"],
    )

        service.add(new_payment)
    await service.commit()




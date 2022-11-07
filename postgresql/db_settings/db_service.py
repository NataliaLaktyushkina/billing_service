import secrets
import string
from typing import List, Optional

from werkzeug.security import generate_password_hash

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import User, PaymentsNew

from sqlalchemy.exc import IntegrityError


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
                    user_id=payment['user_id'],
                    subscription_type=payment['subscription_type'],
                    payment_date=payment['payment_date'],
                    payment_type=payment['payment_type'],
    )

        service.add(new_payment)
    try:
        await service.commit()
    except IntegrityError:
        raise Exception('Could not add payment')
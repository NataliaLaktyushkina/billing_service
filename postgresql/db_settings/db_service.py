import secrets
import string
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from werkzeug.security import generate_password_hash

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import User, PaymentsNew, Payments, PaymentsStatus
from postgresql.db_settings.logger import logger


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()
    return user


def generate_password():

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    return password


def create_user(username, email, password: Optional[str] = None):
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
        logger.error(msg='Could not add payment')


async def extract_new_payments() -> List[PaymentsNew]:
    async with SessionLocal() as session:
        result = await session.execute(select(PaymentsNew))
        return result.scalars().all()


async def load_data_to_payments(new_payments: List[PaymentsNew]) -> None:
    async with SessionLocal() as session:
        for new_payment in new_payments:
            payment = Payments(
                user_id=new_payment.user_id,
                subscription_type=new_payment.subscription_type,
                status=PaymentsStatus.in_processing,
                payment_date=new_payment.payment_date,
                payment_type=new_payment.payment_type,
    )
            session.add(payment)
        await session.commit()


async def delete_new_payments(new_payments: List[PaymentsNew]) -> None:
    async with SessionLocal() as session:
        for new_payment in new_payments:
            await session.delete(new_payment)
        await session.commit()

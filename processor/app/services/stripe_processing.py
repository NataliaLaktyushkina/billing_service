import stripe
from stripe import PaymentMethod, PaymentIntent

from core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


def generate_card() -> PaymentMethod:
    customers_card = stripe.PaymentMethod.create(
        type='card',
        card={
            'number': '4242424242424242',
            'exp_month': 11,
            'exp_year': 2023,
            'cvc': '314',
        },
    )
    return customers_card


def generate_payment_intent(
        amount: int,
        payment_method: PaymentMethod) -> PaymentIntent:

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='rub',
        payment_method_types=['card'],
        payment_method=payment_method,
        description='payment for movie subscription',
        receipt_email='education_tests@mail.ru',
    )

    return payment_intent


def process_payment(amount: int) -> PaymentIntent:
    # Receipts for payments created using test API keys are not sent automatically.
    # Instead, you can view or manually send a receipt using the Dashboard.
    customers_card = generate_card()
    payment_intent = generate_payment_intent(
        amount=amount,
        payment_method=customers_card,
    )

    resp_conf = stripe.PaymentIntent.confirm(
        payment_intent.id,
        payment_method=customers_card.id,
    )

    return resp_conf

import stripe
from stripe import Customer, Product, Price, Subscription
from stripe import SetupIntent

from processor.app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


def generate_product(name: str) -> Product:
    """Products describe the specific goods or services you offer to  customers"""
    return stripe.Product.create(name=name)


def search_product() -> Product:
    product = stripe.Product.search(
        query="name:'movie_subscription'", limit=1,
    )
    return product.data[0]


def create_price(
        new_price: int, interval: str,
        interval_count: int,
) -> Price:
    product = search_product()
    new_price = stripe.Price.create(
        unit_amount=new_price,
        currency='rub',
        recurring={'interval': interval,
                   'interval_count': interval_count},
        product=product.id,
        lookup_key='_'.join((interval, str(interval_count))),
    )
    return new_price


def create_customer(user_id: str, email: str) -> Customer:
    new_customer = stripe.Customer.create(
        name=user_id,
        email=email,
    )
    return new_customer


def create_setup_intent(customer: Customer) -> SetupIntent:
    customers_setup_intent = stripe.SetupIntent.create(
        payment_method='pm_card_visa',
        confirm=True,
        customer=customer.id,
    )
    return customers_setup_intent


def create_subscription(
        customer: Customer, price: Price,setup_intent: SetupIntent,
) -> Subscription:
    """Creates a new subscription on an existing customer."""
    new_subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[
            {'price': price.id},
        ],
        currency='rub',
        description='Movie subscription',
        collection_method='charge_automatically',
        expand=['latest_invoice.payment_intent'],
        default_payment_method=setup_intent.payment_method,
    )
    return new_subscription


def process_payment(
        user_id: str, email: str,
        interval: str, interval_count: int,
) -> Subscription:
    product = search_product()
    price = stripe.Price.search(
        query=f"product:'{product.id}' AND lookup_key:'{interval}_{interval_count}'",
    )
    customer = stripe.Customer.search(
        query=f"name:'{user_id}'",
    )
    if customer.data:
        customer = customer.data[0]
    else:
        customer = create_customer(user_id=user_id, email=email)
    setup_intent = create_setup_intent(customer=customer)
    subscription = create_subscription(
        customer=customer, price=price.data[0],
        setup_intent=setup_intent,
    )

    return subscription


if __name__ == '__main__':
    user_id = '867543fc-886b-49f3-b614-d4120cc3676a'
    email = 'education_tests@mai.ru'
    process_payment(user_id=user_id,
                    email=email)

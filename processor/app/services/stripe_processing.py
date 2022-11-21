import stripe
from stripe import PaymentMethod, PaymentIntent, SetupIntent
from stripe import Customer, Product, Price, Subscription

from processor.app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


def generate_product(name: str) -> Product:
    """Products describe the specific goods or services you offer to  customers"""
    return stripe.Product.create(name=name)


def create_price(
        new_price: int, interval: str,
        interval_count: int, product: Product
) -> Price:
    new_price = stripe.Price.create(
        unit_amount=new_price,
        currency='rub',
        recurring={"interval": interval,
                   'interval_count': interval_count},
        product=product.id,
        lookup_key='_'.join((interval, str(interval_count)))
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
        customer=customer.id
    )
    return customers_setup_intent


def create_subscription(
        customer: Customer, price: Price,setup_intent: SetupIntent
) -> Subscription:
    """Creates a new subscription on an existing customer."""
    new_subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[
            {'price': price.id}
        ],
        currency='rub',
        description='Movie subscription',
        collection_method='charge_automatically',
        expand=['latest_invoice.payment_intent'],
        default_payment_method=setup_intent.payment_method
    )
    return new_subscription


def process_payment(user_id: str,
                    email: str) -> PaymentIntent:
    # Receipts for payments created using test API keys are not sent automatically.
    # Instead, you can view or manually send a receipt using the Dashboard.
    product = stripe.Product.search(
        query="name:'movie_subscription'", limit=1,
    )
    price = stripe.Price.search(
        query=f"product:'{product.data[0].id}' AND lookup_key:'month_1'"
    )

    customer = stripe.Customer.search(
        query=f"name:'{user_id}'"
    )
    if customer.data:
        customer = customer.data[0]
    else:
        customer = create_customer(user_id=user_id, email=email)
    setup_intent = create_setup_intent(customer=customer)
    # stripe.SetupIntent.confirm(
    #     setup_intent.id,
    #     payment_method='pm_card_visa'
    # )
    subscription = create_subscription(customer=customer, price=price.data[0],
                                       setup_intent=setup_intent)

    # payment_intent = subscription.latest_invoice.payment_intent
    # resp_conf = stripe.PaymentIntent.confirm(
    #     payment_intent.id,
    #     payment_method=customer.default_source
    # )
    #
    # return resp_conf
    return subscription
# subscription.status=='active


if __name__ == '__main__':
    user_id = '867543fc-886b-49f3-b614-d4120cc3676a'
    email = 'education_tests@mai.ru'
    process_payment(user_id=user_id,
                    email=email)

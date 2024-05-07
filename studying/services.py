import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_product(product):
    """Create stripe product"""
    stripe_product = stripe.Product.create(name=product.title)
    return stripe_product.id


def create_price(amount):
    """Create stripe price"""
    stripe_price = stripe.Price.create(product.price, currency='rub', amount=amount * 100, product_data={"name": "Payment"})
    return stripe_price.id


def create_session(price):
    """Create stripe session"""
    stripe_session = stripe.checkout.Session.create(success_url="", line_items=price, mode="payment")
    return stripe_session.url

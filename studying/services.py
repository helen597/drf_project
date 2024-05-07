import stripe


def create_product(product):
    stripe_product = stripe.Product.create(name=product.title)
    return stripe_product.id


def create_price(product):
    stripe.Price.create(product.price, currency='RUR')


def create_session():
    pass

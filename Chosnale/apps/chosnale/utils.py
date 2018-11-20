# order_by strings we accept
order_types = ['featured', 'votes', 'pub_date']


def get_order(obj, order):
    return getattr(obj, order)

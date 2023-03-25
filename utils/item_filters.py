def has_price(item):
    return item['price']

def within_budget(item, budget):
    return item['price'] < budget * 100

def under_max_price(item, max_price):
    return item['price'] < max_price * 100

def has_discount(item):
    return item['discount']

def get_price(item):
    return item['price'] / 100.0

def is_game(item):
    return item['type'] == "Game"
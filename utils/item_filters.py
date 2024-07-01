def has_price(item):
    return item['price']

def within_budget(price, budget):
    return float(price) < budget * 100

def under_max_price(price, max_price):
    return float(price) < max_price * 100

def has_discount(item):
    return item['discount']

def get_price(price):
    return float(price) / 100.0

def is_game(item):
    return item['type'] == "Game"

def is_excluded(item, exclusions):
    return item['gameid'][1] in exclusions

def has_tag(item, tag):
    if not tag:
        return True
    return tag in item['tags']

def filter_games(data, **kwargs):
    budget = kwargs.get('budget')
    max_game_price = kwargs.get('max_game_price')
    exclusions = kwargs.get('exclusions', [])
    discount_only = kwargs.get('discount_only', False)
    game_only = kwargs.get('game_only', False)
    tag = kwargs.get('tag', None)

    games = [{
        'appid': item['gameid'][1].lstrip('app/'),
        'title': item['title'],
        'price': get_price(item['price']),
        'discount': item['discount'],
        'url': item['url'],
        'tags': item['tags']
    } for item in data['data'] if has_price(item) and
        within_budget(item['price'], budget) and
        under_max_price(item['price'], max_game_price) and
        (not discount_only or has_discount(item)) and
        (not game_only or is_game(item)) and
        not is_excluded(item, exclusions) and 
        has_tag(item, tag)]
    return games

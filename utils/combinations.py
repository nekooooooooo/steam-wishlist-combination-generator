import random

def random_combination(games, budget, min_spend=0):
    """
    Generate a random combination of games that can be bought within the budget and with a minimum spend of min_spend.
    :param games: list of tuples, where each tuple represents a game title, its price, and discount
    :param budget: float, maximum amount that can be spent
    :param min_spend: float, minimum amount that must be spent
    :return: tuple, where the first element is a list of tuples representing the selected games and their prices, and 
             the second element is the total price of the combination
    """
    
    # Loop until a valid combination is generated
    while True:
        # Select a random number of games from the list
        combo = random.sample(games, random.randint(1, len(games)))
        
        # Calculate the total price of the combination
        total_price = sum(item['price'] for item in combo)
        
        # Check if the total price is within the budget and meets the minimum spend requirement
        if min_spend <= total_price <= budget:
            break

    return combo, total_price
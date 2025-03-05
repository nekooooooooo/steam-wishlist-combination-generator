import random
# from utils.constants import CURRENCY

def random_combination(games, budget, min_spend=0):
    """
    Generate a random combination of games that can be bought within the budget and with a minimum spend of min_spend.
    :param games: list of tuples, where each tuple represents a game title, its price, and discount
    :param budget: float, maximum amount that can be spent
    :param min_spend: float, minimum amount that must be spent
    :return: tuple, where the first element is a list of tuples representing the selected games and their prices, and 
             the second element is the total price of the combination
    """
    MAX_TRIES = 1000

    # Loop until a valid combination is generated
    for i in range(MAX_TRIES):
        # Select a random number of games from the list
        combo = random.sample(games, random.randint(1, len(games)))
        
        # Calculate the total price of the combination
        total_price = sum(item['price'] for item in combo)
        
        # Check if the total price is within the budget and meets the minimum spend requirement
        if min_spend <= total_price <= budget:
            break

        if i == MAX_TRIES - 1:
            print("Error: No valid combination found.")
            break

    return combo, total_price

def print_combination(combo, total_price):
    # Display the games in each combination with their prices and discounts
    print("-" * 97)
    print(f"{'Game':<65} {'Discount'} {'Price':>10}")
    print("=" * 97)
    for item in combo:
        title = item['title']
        discount = item['discount']
        price = item['price']
        print(f"{title:<67} {f'-{discount}%':<9} {price:>10,.2f}")
    print("-" * 97)
    print(f"{'Total price:':<77} {total_price:>10,.2f}\n")
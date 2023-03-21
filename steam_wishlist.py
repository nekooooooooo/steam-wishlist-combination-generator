import time
import json
import random
import os

CURRENCY = "PHP"

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
        total_price = sum(item[1] for item in combo)
        
        # Check if the total price is within the budget and meets the minimum spend requirement
        if min_spend <= total_price <= budget:
            break

    return combo, total_price

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

def get_input(prompt, type_=None, min_=None, max_=None):
    """
    A function that prompts the user for an input and validates it based on the specified type, minimum and maximum values.
    If the input is invalid, it will raise a ValueError with an appropriate error message.
    
    Args:
    - prompt: A string that serves as the prompt for the user input.
    - type_: A type that the user input will be casted into.
    - min_: A number that specifies the minimum allowable value for the user input.
    - max_: A number that specifies the maximum allowable value for the user input.
    
    Returns:
    - value: The validated user input.
    """
    while True:
        try:
            value = type_(input(prompt))
            if min_ is not None and value < min_:
                raise ValueError(f"{prompt} cannot be less than {min_}")
            if max_ is not None and value > max_:
                raise ValueError(f"{prompt} cannot be greater than {max_}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}\n")
    """
    A while loop that continues to prompt the user for an input until a valid input is given.
    A try-except block that attempts to cast the user input into the specified type, and validates the input
    based on the minimum and maximum allowable values. If the input is invalid, it raises a ValueError with
    an appropriate error message. If the input is valid, it returns the validated user input.
    """

def print_combination(combo, total_price, num_combinations):
        # Display the games in each combination with their prices and discounts
        print("-" * 97) 
        print(f"{'Game':<65} {'Discount'} {'Price':>10}")
        print("=" * 97)
        for item in combo:
            print(f"{item[0]:<67} {f'-{item[2]}%':<9} {CURRENCY}{item[1]:>10,.2f}")
        print("-" * 97) 
        print(f"{'Total price:':<77} {CURRENCY}{total_price:>10,.2f}\n")

def main():
    # Load wishlist data from JSON file
    print("Getting wishlist.json")
    with open("wishlist (1).json", encoding="utf-8") as f:
        print("wishlist.json loaded")
        data = json.load(f)

    print(f"Currency: {CURRENCY}")

    # Get user inputs for budget, minimum spend, max game price, and number of combinations
    budget = get_input("Enter your budget: ", float, min_=1)
    min_spend = get_input("Enter your minimum spend: ", float, min_=1, max_=budget)
    max_game_price = get_input("Enter max game price: ", int, min_=1, max_=budget)
    num_combinations = get_input("Enter the number of combinations to generate (up to 5): ", int, min_=1, max_=100) 
    # exclusions = ['app/397540', 'app/349040']
    exclusions = []

    # Filter games from wishlist data based on budget and criteria for games
    games = [
        (item["title"], get_price(item), item['discount'])
        for item in data["data"]
        if has_price(item) and
        within_budget(item, budget) and
        under_max_price(item, max_game_price) and
        has_discount(item) and
        is_game(item) and
        item['gameid'][1] not in exclusions
    ]

    while True:
        # Clear console and generate random game combinations based on user inputs
        os.system('cls')
        print(f"\nGenerating random combination that can be bought within {CURRENCY} {budget} with at least {CURRENCY} {min_spend} spent:\n")
        for i in range(num_combinations):
            combo, total_price = random_combination(games, budget, min_spend)
            if num_combinations != 1:
                print(f"Combination {i + 1}")
            print_combination(combo, total_price, num_combinations)

        # Prompt user to generate more combinations or exit the program
        print(f"\nPress any key to generate {num_combinations} {'combinations' if num_combinations != 1 else 'combination'} again, or")
        user_input = input("Enter the number of combinations to generate (up to 5), or 'e' to exit: ")
        if user_input.lower() == "e":
            break
        elif user_input.isnumeric() and 1 <= int(user_input) <= 5:
            num_combinations = int(user_input)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("%s seconds" % (time.time() - start_time))

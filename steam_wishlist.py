import time
import os
from utils.item_filters import has_price, within_budget, under_max_price, has_discount, get_price, is_game
from utils.combinations import random_combination
from utils.input import get_input
from utils.wishlist_data import get_wishlist_from_steam, get_wishlist_from_file

CURRENCY = "PHP"

def print_combination(combo, total_price):
    # Display the games in each combination with their prices and discounts
    print("-" * 97) 
    print(f"{'Game':<65} {'Discount'} {'Price':>10}")
    print("=" * 97)
    for item in combo:
        title = item['title']
        discount = item['discount']
        price = item['price']
        print(f"{title:<67} {f'-{discount}%':<9} {CURRENCY}{price:>10,.2f}")
    print("-" * 97) 
    print(f"{'Total price:':<77} {CURRENCY}{total_price:>10,.2f}\n")

def main():

    print("Please choose an option:")
    print("[1] Use File")
    print("[2] Use Steam ID/Steam URL")
    option = input("Enter your choice (1 or 2): ")
    while True:
        if option == "1":
            # Load wishlist from file
            data = get_wishlist_from_file("wishlist.json")
            break
        elif option == "2":
            # Load wishlist data from steam
            while True:
                input_id = input("Enter steam id: ")
                data = get_wishlist_from_steam(input_id)
                if data['data']:
                    break
                else:
                    print(f"Sorry, the specified ID could not be found: {input_id}")
            break
        else:
            print("Invalid option. Please enter 1 or 2.")
    

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
        {
            'title': item["title"], 
            'price': get_price(item), 
            'discount': item['discount']
        }
        for item in data["data"]
        if has_price(item) and
        within_budget(item, budget) and
        under_max_price(item, max_game_price) and
        # has_discount(item) and
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
            print_combination(combo, total_price)

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

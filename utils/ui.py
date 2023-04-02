import customtkinter as ctk
import tkinter as tk
from customtkinter import filedialog
from tkinter import messagebox
from utils.item_filters import filter_games
from utils.combinations import random_combination, print_combination
from utils.input import get_input
from utils.wishlist_data import get_wishlist_from_steam, get_wishlist_from_file
from utils.constants import CURRENCY

ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

WIDTH = 800
HEIGHT = 400

class MethodTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("File")
        self.add("SteamID")
        self.tab("File").grid_columnconfigure((0, 2), weight=0)
        self.tab("File").grid_columnconfigure(1, weight=1)
        self.tab("SteamID").grid_columnconfigure((0, 2), weight=0)
        self.tab("SteamID").grid_columnconfigure(1, weight=1)

        self.filepath_label = ctk.CTkLabel(self.tab("File"), text="File Path:")
        self.filepath_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.filepath_entry = ctk.CTkEntry(self.tab("File"))
        self.filepath_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.file_button = ctk.CTkButton(self.tab("File"), text="Select File", command=self.select_file)
        self.file_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.steamid_label = ctk.CTkLabel(self.tab("SteamID"), text="SteamID:")
        self.steamid_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.steamid_entry = ctk.CTkEntry(self.tab("SteamID"))
        self.steamid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    def select_file(self):
        # Open a file dialog to select a file
        filepath = filedialog.askopenfilename()
        
        # Update the file path entry widget with the selected file path
        self.filepath_entry.delete(0, ctk.END)
        self.filepath_entry.insert(0, filepath)

class WishlistGeneratorUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steam Wishlist Generator")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        self.theme_button = ctk.CTkButton(self, text="Toggle Theme", command=self.theme_toggle)
        self.theme_button.grid(row=3, column=0, padx=10, pady=10)

        self.method_tab = MethodTab(master=self, width=250, height=0)
        self.method_tab.grid(row=0, column=0, columnspan=3, padx=(10), pady=(10, 0), sticky="nsew")

        self.get_button = ctk.CTkButton(self, text="Get", command=self.get_wishlist_from_id)
        self.get_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def get_wishlist_from_id(self):
        if self.method_tab.get() == "File":
            filepath = self.method_tab.filepath_entry.get()
            data = get_wishlist_from_file(filepath)
        else:
            steamid = self.method_tab.steamid_entry.get()
            data = get_wishlist_from_steam(steamid)
            if not data['data']:
                messagebox.showerror("SteamID Error", f"Sorry, the specified ID could not be found: {steamid}")

    def theme_toggle(self):
        appearance_mode = "light" if ctk.get_appearance_mode() == "Dark" else "dark"
        ctk.set_appearance_mode(appearance_mode)
        


#     print("Please choose an option:")
#     print("[1] Use File")
#     print("[2] Use Steam ID/Steam URL")
#     while True:
#         option = input("Enter your choice (1 or 2): ")
#         if option == "1":
#             # Load wishlist from file
#             data = get_wishlist_from_file("wishlist.json")
#             break
#         elif option == "2":
#             # Load wishlist data from steam
#             while True:
#                 input_id = input("Enter steam id: ")
#                 data = get_wishlist_from_steam(input_id)
#                 if data['data']:
#                     break

#                 print(f"Sorry, the specified ID could not be found: {input_id}")
#             break

#         print("Invalid option. Please enter 1 or 2.")

#     # print(f"Currency: {CURRENCY}")

#     # Get user inputs for budget, minimum spend, max game price, and number of combinations
#     budget = get_input("Enter your budget: ", float, min_=1)
#     min_spend = get_input("Enter your minimum spend: ",float, min_=1, max_=budget)
#     max_game_price = get_input("Enter max game price: ", int, min_=1, max_=budget)
#     num_combinations = get_input("Enter the number of combinations to generate (up to 5): ", int, min_=1, max_=100)
#     discount_only = input("Only discounted games? (Y/N): ").lower() == "y"
#     # exclusions = ['app/397540', 'app/349040']
#     exclusions = []

#     # Filter games from wishlist data based on budget and criteria for games
#     games = filter_games(data, budget, max_game_price, exclusions, discount_only)

#     while True:
#         # Clear console and generate random game combinations based on user inputs
#         os.system('cls')
#         print(f"\nGenerating random combination that can be bought within {CURRENCY} {budget} with at least {CURRENCY} {min_spend} spent:\n")
#         for i in range(num_combinations):
#             combo, total_price = random_combination(games, budget, min_spend)
#             if num_combinations != 1:
#                 print(f"Combination {i + 1}")
#             print_combination(combo, total_price)

#         # Prompt user to generate more combinations or exit the program
#         print(f"\nPress any key to generate {num_combinations} {'combinations' if num_combinations != 1 else 'combination'} again, or")
#         user_input = input("Enter the number of combinations to generate (up to 5), or 'e' to exit: ")
#         if user_input.lower() == "e":
#             break
#         elif user_input.isnumeric() and 1 <= int(user_input) <= 5:
#             num_combinations = int(user_input)
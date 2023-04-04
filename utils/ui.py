import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip
from customtkinter import filedialog
from tkinter import messagebox
from utils.item_filters import filter_games
from utils.combinations import random_combination, print_combination
from utils.input import get_input
from utils.wishlist_data import get_wishlist_from_steam, get_wishlist_from_file
from utils.constants import CURRENCY

ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

MIN_WIDTH = 750
MIN_HEIGHT = 600

class MethodTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("SteamID")
        self.add("File")
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

        self.steamid_entry = ctk.CTkEntry(self.tab("SteamID"), placeholder_text="SteamID32, URL, or Custom URL")
        self.steamid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


    def select_file(self):
        # Open a file dialog to select a file
        filepath = filedialog.askopenfilename()
        
        # Update the file path entry widget with the selected file path
        self.filepath_entry.delete(0, ctk.END)
        self.filepath_entry.insert(0, filepath)

class InputsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2), weight=1)
        vcmd = (self.register(self.callback))

        # add widgets onto the frame...
        self.budget_label = ctk.CTkLabel(self, text="Budget")
        self.budget_label.grid(row=0, column=0, padx=10, pady=0, sticky="ew")
        self.budget_entry = ctk.CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.budget_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.minimum_label = ctk.CTkLabel(self, text="Minimum Spend")
        self.minimum_label.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        self.minimum_entry = ctk.CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.minimum_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew")

        self.max_price_entry = ctk.CTkLabel(self, text="Maximum Game Price")
        self.max_price_entry.grid(row=0, column=2, padx=10, pady=0, sticky="ew")
        self.max_price_entry = ctk.CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.max_price_entry.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="nsew")

        self.game_only_switch = ctk.CTkSwitch(self, text="Game only?")
        self.game_only_switch.grid(row=2, column=0, padx=10, pady=(10, 0))

        self.discount_only_switch = ctk.CTkSwitch(self, text="Discounted only?")
        self.discount_only_switch.grid(row=2, column=1, padx=10, pady=(10, 0))

        self.exclusions_entry = ctk.CTkLabel(self, text="Exclusions", anchor="w")
        self.exclusions_entry.grid(row=3, column=0, padx=10, pady=0, sticky="ew")
        self.exclusions_entry = ctk.CTkEntry(self, placeholder_text="Use game app id, separate with comma")
        self.exclusions_entry.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")
    

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

class OutputsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0)
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.columns = ['title', 'discount', 'price']
        self.output_tree = ttk.Treeview(self, columns=self.columns, show='headings', style="mystyle.Treeview")
        self.output_tree.tag_configure('odd', background='#E8E8E8')
        self.output_tree.tag_configure('even', background='#DFDFDF')

        # Define the columns
        self.output_tree.heading('title', text='Title')
        self.output_tree.heading('discount', text='Discount', anchor="e")
        self.output_tree.heading('price', text='Price', anchor="e")

        self.output_tree.column("title", width=200)
        self.output_tree.column("discount", width=25)
        self.output_tree.column("price", width=30)


class WishlistGeneratorUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steam Wishlist Generator")
        self.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.data = []

        self.method_tab = MethodTab(master=self, width=250, height=0)
        self.method_tab.grid(row=0, column=0, columnspan=5, padx=(10), pady=(10, 0), sticky="nsew")

        self.input_frame = InputsFrame(master=self)
        self.input_frame.grid(row=1, column=0, columnspan=5, padx=(10), pady=(10, 0), sticky="nsew")

        self.get_button = ctk.CTkButton(self, text="Get", command=self.get_button_callback)
        self.get_button.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.output_frame = OutputsFrame(master=self)
        self.output_frame.grid(row=3, column=0, columnspan=5, padx=(10), pady=(10, 0), sticky="nsew")

        self.total_label = ctk.CTkLabel(self, text="Total: ")
        self.total_label.grid(row=4, column=0, padx=10, pady=0, sticky="ew")
        
        # self.theme_button = ctk.CTkButton(self, text="Toggle Theme", command=self.theme_toggle)
        # self.theme_button.grid(row=6, column=0, padx=10, pady=10)

    def get_button_callback(self):
        
        if not self.data:
            if self.method_tab.get() == "File":
                filepath = self.method_tab.filepath_entry.get()
                self.data = get_wishlist_from_file(filepath)
            else:
                steamid = self.method_tab.steamid_entry.get()
                self.data = get_wishlist_from_steam(steamid)
                if not self.data['data']:
                    messagebox.showerror("SteamID Error", f"Sorry, the specified ID could not be found: {steamid}")

        budget = int(self.input_frame.budget_entry.get())
        min_spend = int(self.input_frame.minimum_entry.get())
        max_game_price = int(self.input_frame.max_price_entry.get())
        game_only = bool(self.input_frame.game_only_switch.get())
        discount_only = bool(self.input_frame.discount_only_switch.get())
        exclusions = self.input_frame.exclusions_entry.get()
        format_exclusions = self.format_app_ids(exclusions) if exclusions else []

        if not budget:
            return messagebox.showerror("Input Error", "Budget can't be empty!")

        if not min_spend:
            return messagebox.showerror("Input Error", "Minimum Spend can't be empty!")

        if not max_game_price:
            return messagebox.showerror("Input Error", "Max Price can't be empty!")

        if min_spend > budget or max_game_price > budget:
            return messagebox.showerror("Input Error", "Minimum Spend or Max Price can't be more than budget!")

        games = filter_games(self.data, budget, max_game_price, format_exclusions, discount_only, game_only)
        combo, total_price = random_combination(games, budget, min_spend)

        self.output_frame.output_tree.delete(*self.output_frame.output_tree.get_children())

        for i, item in enumerate(combo):
            tag = "even" if (i + 1) % 2 == 0 else "odd"
            values = (
                item['title'],
                f"{item['discount']}%",
                item['price']
            )
            self.output_frame.output_tree.insert('', 'end', values=values, tags=(tag,))

        self.output_frame.output_tree.pack(fill='both', expand=True)
        self.total_label.configure(text=f"Total: {total_price}")

        # print(f"{title:<67} {f'-{discount}%':<9} {CURRENCY}{price:>10,.2f}")
        # print(f"\nGenerating random combination that can be bought within {CURRENCY} {budget} with at least {CURRENCY} {min_spend} spent:\n")
        # combo, total_price = random_combination(games, budget, min_spend)
        # print_combination(combo, total_price)

    def format_app_ids(self, exclusions):
        return ['app/' + x.strip() for x in exclusions.split(',')]

    def theme_toggle(self):
        appearance_mode = "light" if ctk.get_appearance_mode() == "Dark" else "dark"
        ctk.set_appearance_mode(appearance_mode)
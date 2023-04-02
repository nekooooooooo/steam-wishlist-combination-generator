from utils.constants import STEAM_WISHLIST_VANITY_URL, STEAM_WISHLIST_ID_URL
import json
import requests
from urllib.parse import urlparse
from tqdm import tqdm

def get_wishlist_url(is_vanity):
    if is_vanity:
        return STEAM_WISHLIST_VANITY_URL
    else:
        return STEAM_WISHLIST_ID_URL

def get_wishlist_from_file(file):
    print("Getting wishlist.json")
    with open(f"{file}", 'r', encoding="utf-8") as f:
        print("wishlist.json loaded")
        data = json.load(f)
        return data

def get_wishlist_from_steam(input_id):
    # Extract id from input
    steam_id, is_vanity = get_id(input_id)

    # Send GET request to Steam wishlist URL and get response content
    wishlist_url = get_wishlist_url(is_vanity)
    
    # Get the first page of the wishlist data
    result = []
    page_num = 0
    while True:
        response = requests.get(wishlist_url.format(steam_id, page_num))
        data = json.loads(response.content)

        # Check if data is empty list
        if len(data) == 0 or data.get('success') == 2:
            break
        
        for _, games in tqdm(data.items(), desc=f"Extracting wishlist data page {page_num + 1}"):
            if games['subs']:
                # extract relevant data from the game data
                app_id = f"app/{games['subs'][0]['id']}"
                title = games['name'].replace("'", "\'")
                game_type = games['type']
                price = games['subs'][0]['price']
                discount = games['subs'][0]['discount_pct']

                # create the new dictionary
                game_dict = {
                    "gameid": ["steam", app_id],
                    "title": title,
                    "type": game_type,
                    "price": price,
                    "discount": discount
                }

                # add it to the result list
                result.append(game_dict)

        page_num += 1

    wishlist = {"data": result}
    return wishlist

def get_id(input_id):
    if "https://steamcommunity.com" in input_id:
        # Parse the URL and get the path component
        path = urlparse(input_id).path

        # Split the path on the '/' character
        path_parts = path.split('/')

        # Check if the first part of the path is 'id' or 'profiles'
        if path_parts[1] == 'id':
            # Custom ID format
            return path_parts[2], True

        # Steam ID format
        return path_parts[2], False

    # it's a custom ID
    if not input_id.isnumeric():
        return input_id, True

    return input_id, False
            

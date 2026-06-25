from utils.constants import STEAM_WISHLIST_API_URL, STEAM_APPDETAILS_API_URL, COUNTRY_CODE
import json
import requests
from urllib.parse import urlparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import os

type_map = {
    "game": "Game",
    "dlc": "DLC",
    "demo": "Demo",
    "music": "Music",
    "movie": "Video",
    "video": "Video",
    "series": "Series",
    "mod": "Mod",
    "advertising": "Advertising",
    "hardware": "Hardware",
    "software": "Software",
}

_session = requests.Session()
_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
})

_cache_file = "appdetails_cache.json"
_cache_ttl = 3600
_cache = {}

def _load_cache():
    global _cache
    if os.path.exists(_cache_file):
        try:
            with open(_cache_file, 'r', encoding="utf-8") as f:
                _cache = json.load(f)
        except:
            _cache = {}
    else:
        _cache = {}

def _save_cache():
    try:
        with open(_cache_file, 'w', encoding="utf-8") as f:
            json.dump(_cache, f, indent=2)
    except:
        pass

_load_cache()

def get_wishlist_from_file(file):
    print("Getting wishlist.json")
    with open(f"{file}", 'r', encoding="utf-8") as f:
        print("wishlist.json loaded")
        data = json.load(f)
        return data

def fetch_app_details(appid):
    now = time.time()
    cached = _cache.get(str(appid))
    if cached and now - cached.get("timestamp", 0) < _cache_ttl:
        return cached["data"]

    for attempt in range(3):
        try:
            r = _session.get(
                STEAM_APPDETAILS_API_URL,
                params={"appids": appid, "cc": COUNTRY_CODE},
                timeout=10
            )
            if not r.ok:
                time.sleep(1 * (attempt + 1) + random.random())
                continue

            resp = r.json().get(str(appid), {})
            if not resp.get("success"):
                _cache[str(appid)] = {"data": None, "timestamp": now}
                _save_cache()
                return None

            data = resp["data"]
            if data.get("is_free"):
                _cache[str(appid)] = {"data": None, "timestamp": now}
                _save_cache()
                return None
            price = data.get("price_overview")
            if not price:
                _cache[str(appid)] = {"data": None, "timestamp": now}
                _save_cache()
                return None

            game_type = type_map.get(data.get("type", ""), data.get("type", "").title())

            game_dict = {
                "gameid": ["steam", f"app/{appid}"],
                "title": data["name"],
                "type": game_type,
                "price": price["final"],
                "discount": price["discount_percent"],
                "capsule": data.get("header_image", ""),
                "url": f"https://store.steampowered.com/app/{appid}",
                "tags": [g["description"] for g in data.get("genres", [])]
            }

            _cache[str(appid)] = {"data": game_dict, "timestamp": now}
            _save_cache()
            return game_dict

        except requests.RequestException:
            if attempt < 2:
                time.sleep(1 * (attempt + 1) + random.random())
                continue
            return None
        except Exception:
            return None
    return None

def get_wishlist_from_steam(input_id):
    steam_id, _ = get_id(input_id)

    r = requests.get(STEAM_WISHLIST_API_URL, params={"steamid": steam_id}, timeout=15,
                     headers={"User-Agent": _session.headers["User-Agent"]})
    data = r.json()
    items = data.get("response", {}).get("items", [])
    if not items:
        return {"data": []}

    appids = [item["appid"] for item in items]

    result = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_app_details, appid): appid for appid in appids}
        for future in tqdm(as_completed(futures), total=len(appids), desc="Fetching game details"):
            game_dict = future.result()
            if game_dict:
                result.append(game_dict)

    return {"data": result}

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
            

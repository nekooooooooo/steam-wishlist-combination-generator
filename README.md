![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-cord?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/nekooooooooo/salty-dream-bot?style=for-the-badge)

# Steam Wishlist Combination Generator

A simple, unoptimized python script that helps me decide which games to buy from my wishlist.

![Steam Wishlist Preview](https://raw.githubusercontent.com/nekooooooooo/nekooooooooo.github.io/master/pics/preview_steam_wishlist_3.png)

> ⚠ **Notice**  
> As of **November 2024**, the old wishlist API endpoints stopped working.  
> The script now uses the official Steam Web API (`IWishlistService/GetWishlist/v1`)  
> to fetch wishlist data via SteamID.

This script can fetch wishlist data using either a json file from [Augmented Steam](https://github.com/IsThereAnyDeal/AugmentedSteam) or directly from Steam's API by entering a SteamID64.

## Setup and Usage

- Clone this repository
- `pip install -r requirements.txt`
- Run script

Optionally

- Install [Augmented Steam](https://augmentedsteam.com/)

![Chrome download link](https://developer.chrome.com/static/docs/webstore/branding/image/UV4C4ybeBTsZt43U4xis.png) [![Firefox download link](https://extensionworkshop.com/assets/img/documentation/publish/get-the-addon-178x60px.dad84b42.png)](https://addons.mozilla.org/firefox/addon/augmented-steam/)

- Export your wishlist to a json file named `wishlist.json`

## Optional Variables

Change the pricing region inside `utils/constants.py`:

```py
COUNTRY_CODE = "ph"  # two-letter country code for Steam pricing
```

A cache of fetched app details is stored in `appdetails_cache.json` (1-hour TTL) to reduce API calls. Delete this file to force a fresh fetch.

## Credits

- TomSchimansky for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- IsThereAnyDeal for Augmented Steam

## To Do (Some planned features might be added to web version)

- [ ] Optimize code
- [x] GUI using Tkinter, maybe (04/04/2023)
    - [x] Clickable links (04/04/2023)
    - [ ] Game Banner Preview
- [ ] More options
    - [x] Is Game toggle (04/04/2023)
    - [x] Is discounted toggle (04/04/2023)
    - [ ] Discount minimum - maximum
    - [ ] has Cards toggle
    - [ ] has Achievements toggle
    - [ ] Tags selection
    - [ ] Currency Change
    - [x] Exclusions (04/04/2023)
- [ ] Display all games from wishlist
- [ ] Edit output
    - [ ] Add/Remove Games
    - [ ] Generate list with remaining funds
- [x] Support for official steam wishlist data json (26/3/2023)
    - [x] Steam URL/SteamID/Vanity Url
- [ ] Sort
- [x] Executable release
- [ ] CLI release
- [ ] Web app release

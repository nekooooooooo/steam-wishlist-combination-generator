![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-cord?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/nekooooooooo/salty-dream-bot?style=for-the-badge)

# Steam Wishlist Combination Generator

A simple, unoptimized python script that helps me decide which games to buy from my wishlist.

![](https://raw.githubusercontent.com/nekooooooooo/nekooooooooo.github.io/master/pics/preview_steam_wishlist_3.png)

This script uses [Augmented Steam's](https://github.com/IsThereAnyDeal/AugmentedSteam) wishlist export to json function.

## Setup and Usage
- Clone this repository
- `pip install -r requirements.txt`
- Run script

Optionally
- Install [Augmented Steam](https://augmentedsteam.com/)

[![Chrome download link](https://storage.googleapis.com/web-dev-uploads/image/WlD8wC6g8khYWPJUsQceQkhXSlv1/UV4C4ybeBTsZt43U4xis.png)](https://chrome.google.com/webstore/detail/augmented-steam/dnhpnfgdlenaccegplpojghhmaamnnfp) [![Firefox download link](https://extensionworkshop.com/assets/img/documentation/publish/get-the-addon-178x60px.dad84b42.png)](https://addons.mozilla.org/firefox/addon/augmented-steam/)
- Export your wishlist to a json file named `wishlist.json`

## Optional variables:

Optionally, change currency inside the utils/constants.py, line 3 `CURRENCY = "<currency>"`, currently it's in my currency but it should work still
```py
CURRENCY = "<currency>"
```

## Credits
- TomSchimansky for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- IsThereAnyDeal for Augmented Steam

## To Do
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
- [ ] Logging
- [ ] Executable release
- [ ] CLI release

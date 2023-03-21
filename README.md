![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-cord?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/nekooooooooo/salty-dream-bot?style=for-the-badge)

# Steam Wishlist Combination Generator

A simple, unoptimized python script that helps me decide which games to buy from my wishlist.

![](https://raw.githubusercontent.com/nekooooooooo/nekooooooooo.github.io/master/pics/preview_steam_wishlist.png)

This script uses [Augmented Steam's](https://github.com/IsThereAnyDeal/AugmentedSteam) wishlist export to json function.

## Setup and Usage

- Install [Augmented Steam](https://augmentedsteam.com/)

[![Chrome download link](https://storage.googleapis.com/web-dev-uploads/image/WlD8wC6g8khYWPJUsQceQkhXSlv1/UV4C4ybeBTsZt43U4xis.png)](https://chrome.google.com/webstore/detail/augmented-steam/dnhpnfgdlenaccegplpojghhmaamnnfp) [![Firefox download link](https://extensionworkshop.com/assets/img/documentation/publish/get-the-addon-178x60px.dad84b42.png)](https://addons.mozilla.org/firefox/addon/augmented-steam/)
- Export your wishlist to a json file named `wishlist.json`
- Clone this repository
- Place `wishlist.json` inside `../steam-wishlist-combination`
- Optionally, change currency inside the code (will create a config for this maybe) currently it's in my currency but it should work still
- Run script

## Credits
- IsThereAnyDeal for Augmented Steam

## To Do
- [ ] Optimize code
- [ ] GUI using Tkinter, maybe
    - [ ] Clickable links
    - [ ] Game Banner Preview
- [ ] More options
    - [ ] Is Game toggle
    - [ ] Is discounted toggle
    - [ ] Discount minimum - maximum
    - [ ] has Cards toggle
    - [ ] has Achievements toggle
    - [ ] Tags selection
- [ ] Support for official steam wishlist data json

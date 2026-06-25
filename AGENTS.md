# Steam Wishlist Combination Generator - Agent Guide

## Project Overview
Python GUI app (CustomTkinter) that generates game purchase combinations from a Steam wishlist within a budget.

## Quick Start
```bash
# Use the existing venv
.venv\Scripts\activate
pip install -r requirements.txt
python steam_wishlist.py
```

## Key Commands
- **Run**: `python steam_wishlist.py`
- **Install deps**: `pip install -r requirements.txt`
- No formal test/lint/typecheck commands configured

## Architecture
- **Entry point**: `steam_wishlist.py` → `utils.ui.WishlistGeneratorUI`
- **Package**: `utils/` (ui, combinations, item_filters, wishlist_data, constants, input)
- **GUI**: CustomTkinter with ttk.Treeview for results table
- **Data sources**: 
  - File: `wishlist.json` (Augmented Steam export) via `get_wishlist_from_file()`
  - Steam API: `get_wishlist_from_steam()` — **broken as of Nov 2024** (Steam changed API)

## Important Notes
- SteamID input tab is hidden in UI (`MethodTab.delete("SteamID")` at ui.py:44)
- Currency configurable in `utils/constants.py:CURRENCY` (line 3)
- Exclusions use Steam app IDs prefixed with `app/` (see `format_app_ids()` at ui.py:268)
- Prices stored as integers (cents) in wishlist data, converted to float for display
- Output executable at `output/steam_wishlist.exe` (gitignored)
- Virtual env at `.venv/` (gitignored)
- `utils/input.py` exists but is unused in current GUI code path (legacy CLI helper)
- `config/` directory is empty (only `__pycache__`)
- `appdetails_cache.json` in root is a runtime cache file (gitignored via `*.json`)

## Files to Ignore
- `.venv/`, `output/`, `__pycache__/`, `*.json`, `test*.py`, `old.py`, `tempCodeRunnerFile.python`, `.vscode/`, `config/`
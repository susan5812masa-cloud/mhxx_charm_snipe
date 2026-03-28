# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MHXX (Monster Hunter XX) charm sniping automation. Combines OCR-based charm reading, RNG frame analysis, and Arduino-based Nintendo Switch controller automation to hit specific frames for desired charms.

## No Build System

This project has no package manager or build system. Dependencies:
- Python: `opencv-python`, `numpy`, `pytesseract`
- Tesseract OCR installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Arduino IDE with `NintendoSwitchControlLibrary.h`
- Git submodule: `capture/mhxx-rng-main/` (RNG solver — must be initialized)

Initialize submodule after cloning:
```bash
git submodule update --init --recursive
```

Run Python scripts directly:
```bash
python capture/capture_test.py     # Webcam capture (SPACE to screenshot)
python capture/check_region.py     # Extract charm regions from screenshot
python capture/read_talisman.py    # OCR + RNG frame search (main pipeline)
python capture/find_frame.py       # RNG frame search only
python capture/ocr_test.py         # OCR test on a single image
```

## Architecture

The pipeline runs in sequence:

```
[Webcam] → capture_test.py → screenshots/
         → check_region.py → region crops (skill1, skill2, slots)
         → read_talisman.py → OCR via Tesseract → fuzzy skill matching
         → find_frame.py → RNG frame search (via mhxx-rng-main submodule)
         → talisman_log.csv + frame number
         → Arduino uses frame number → calculates button timing → inputs to Switch
```

### Python (`capture/`)

- **`read_talisman.py`** — Main entry point. Reads a talisman screenshot, extracts skills/slots via OCR, then calls `find_frame.py` to find the RNG frame. Writes results to `talisman_log.csv`.
- **`find_frame.py`** — Converts OCR skill names to RNG internal format, searches frames 0–10^7 using the submodule's RNG algorithm.
- **`check_region.py`** — Crops fixed pixel regions from 1920×1080 screenshots: panel (y:130–500, x:700–1300), skill1 (y:245–290, x:950–1300), skill2 (y:285–330, x:950–1300), slots (y:330–375, x:700–1000).
- **`capture_test.py`** — Captures 1920×1080 frames from webcam device 0; SPACE saves a screenshot.
- **`ocr_test.py`** — Standalone OCR testing.

OCR uses dual-mode processing (normal + color-inverted) with a correction dictionary for common Tesseract misreadings of Japanese skill names, and fuzzy matching against a hardcoded database of 80+ known MHXX skills.

### Arduino (`arduino/mhxx-rng-long/`)

`mhxx-rng-long.ino` emulates a Switch Pro Controller. Key calibration constants that must be tuned per-environment:

| Constant | Purpose |
|---|---|
| `TARGET_FRAME` | Target RNG frame for the desired charm |
| `ADJUST_F` | Per-environment calibration offset |
| `FC` | Frame cost per continue button press |
| `F_BEFORE_MS` / `F_AFTER_MS` | Frame cost per ms for pre/post delay |
| `BASE_CONST` | Fixed frame overhead |

Pin assignments: Button=2, Green LED=3 (running), Red LED=4 (done).

### Submodule (`capture/mhxx-rng-main/`)

External RNG solver from `apmnnn/mhxx-rng`. Contains the Jupyter notebook (`mhxx-rng.ipynb`) with the core RNG algorithm. `find_frame.py` imports from this submodule to iterate frames.

## Key Data

Skill names are stored in two forms in `read_talisman.py`: full Japanese names and abbreviated versions (e.g., `攻撃力UP【大】` → `攻撃大`). The mapping between OCR output and RNG internal skill IDs is defined in `find_frame.py`.

Output is appended to `capture/talisman_log.csv` (gitignored).

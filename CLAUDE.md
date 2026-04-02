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

**ボード: Arduino Leonardo**（UNO ではない。コード記述時に重要）

`mhxx-rng-long.ino` emulates a Switch Pro Controller. Key calibration constants that must be tuned per-environment:

| Constant | Purpose |
|---|---|
| `TARGET_FRAME` | Target RNG frame for the desired charm |
| `ADJUST_F` | Per-environment calibration offset |
| `FC` | Frame cost per continue button press |
| `F_BEFORE_MS` / `F_AFTER_MS` | Frame cost per ms for pre/post delay |
| `BASE_CONST` | Fixed frame overhead |

Pin assignments: Button=2, Green LED=3 (running), Red LED=4 (done).

#### Leonardo の Serial に関する注意

Leonardo は UNO と Serial の扱いが異なる。スケッチを書く際に必ず区別すること。

| オブジェクト | 接続先 | 用途 |
|---|---|---|
| `Serial` | USB CDC（ネイティブUSB） | PC との直接通信、デバッグ出力 |
| `Serial1` | D0(RX) / D1(TX) | 外部デバイス（CH340等）との UART 通信 |

本番環境では Arduino USB → Switch 接続のため `Serial`（USB）が HID で占有される。
外部シリアル通信が必要な場合は `Serial1`（D0/D1）を使うこと。

#### PC-Arduino 間シリアル通信（開発・デバッグ時）

CH340G USB-UART 変換モジュール経由で接続する。

```
PC (USB) ── CH340G ── Arduino Leonardo
               TXD → D0 (RX / Serial1)
               RXD ← D1 (TX / Serial1)
               GND → GND
           VCC+5V → 5V  ※Arduino USB を抜いた場合の電源供給
```

- CH340G の電圧ジャンパは **VCC+5V ↔ CH340G VCC**（5Vモード）に設定すること
  - 3.3Vモードにすると TXD 出力が 3.3V になり Arduino（5V系）との通信が不安定になる
- スケッチ書き込み時は CH340G の TX/RX を D0/D1 から**必ず外すこと**
- Arduino USB と CH340G を同時に D0/D1 に接続するとバス競合が起きる
  - デバッグ通信中は Arduino USB を抜き、CH340G の VCC+5V から電源供給する

### Submodule (`capture/mhxx-rng-main/`)

External RNG solver from `apmnnn/mhxx-rng`. Contains the Jupyter notebook (`mhxx-rng.ipynb`) with the core RNG algorithm. `find_frame.py` imports from this submodule to iterate frames.

## Key Data

Skill names are stored in two forms in `read_talisman.py`: full Japanese names and abbreviated versions (e.g., `攻撃力UP【大】` → `攻撃大`). The mapping between OCR output and RNG internal skill IDs is defined in `find_frame.py`.

Output is appended to `capture/talisman_log.csv` (gitignored).

## Debug Tools (`debug/`)

PC-Arduino 間のシリアル通信疎通確認用スクリプト。本番環境への組み込み前の動作確認に使用する。

- `debug/serial_debug/serial_debug.ino` — Arduino 側（`Serial1` 使用）
- `debug/serial_debug.py` — PC 側（pyserial。上部の `COM_PORT` を CH340 のポート番号に書き換えて使用）

動作フロー: PC → `start` 送信 → 緑LED 5回点滅 → Arduino → `done` 送信 → PC → `end` 送信 → 赤LED 5秒点灯 → 待機状態へ

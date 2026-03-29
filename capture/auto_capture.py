"""
auto_capture.py - 自動キャプチャ & 護石読み取り & フレーム誤差算出

【使い方】
  python capture/auto_capture.py <待機秒数>
  例) python capture/auto_capture.py 320

【フロー】
  1. このスクリプトを実行
  2. 「Arduinoのボタンを押してください」と表示されたらボタンを押す
  3. <待機秒数> 後に自動でWebカメラをキャプチャ
  4. OCR → フレーム検索（TARGET_FRAME周辺のみ）→ 誤差を表示

【フェーズ2（将来）】
  Arduinoからシリアル通信で "DONE" を受信したら自動キャプチャ
  → WAIT_MODE = 'serial' に変更し、COMポートを設定する
"""

import cv2
import sys
import os
import time
import ctypes
from datetime import datetime

# ===== Windows スリープ防止 =====
# スクリプト実行中にPCがスリープ・画面オフになるのを防ぐ
_ES_CONTINUOUS       = 0x80000000
_ES_SYSTEM_REQUIRED  = 0x00000001  # スリープ防止
_ES_DISPLAY_REQUIRED = 0x00000002  # 画面オフ防止

def _sleep_prevent():
    ctypes.windll.kernel32.SetThreadExecutionState(
        _ES_CONTINUOUS | _ES_SYSTEM_REQUIRED | _ES_DISPLAY_REQUIRED
    )

def _sleep_allow():
    ctypes.windll.kernel32.SetThreadExecutionState(_ES_CONTINUOUS)

# ===== カメラ設定 =====
CAMERA_INDEX  = 0       # Webカメラのデバイス番号
CAMERA_WIDTH  = 1920
CAMERA_HEIGHT = 1080
CAMERA_WARMUP = 1.0     # カメラ起動後の安定待機（秒）

# ===== 待機モード =====
WAIT_MODE     = 'time'  # 'time' = 時間待ち / 'serial' = シリアル通信（将来）
# SERIAL_PORT = 'COM3'  # フェーズ2で使用
# SERIAL_BAUD = 9600    # フェーズ2で使用

# ===== ★ ターゲットフレーム設定（護石を変えるときに変更する）★ =====
# Arduinoスケッチの TARGET_FRAME と同じ値を設定する
TARGET_FRAME = 702223

# OCR後のフレーム検索範囲: TARGET_FRAME ± SEARCH_MARGIN
# ADJUST_Fの最大対応範囲（±15000F）より十分大きい値にする
SEARCH_MARGIN = 100000

# ===== パス設定 =====
_BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(_BASE_DIR, 'screenshots')

sys.path.insert(0, _BASE_DIR)
from read_talisman import read_talisman, print_result, save_to_csv
from find_frame import find_frame


# ===== カウントダウン =====
def countdown(seconds):
    print(f"\n[待機開始] {seconds}秒後にキャプチャします")
    print("（今すぐArduinoのボタンを押してください）\n")

    start = time.time()
    while True:
        remaining = seconds - (time.time() - start)
        if remaining <= 0:
            break
        mins = int(remaining) // 60
        secs = int(remaining) % 60
        print(f"\r  残り {mins:02d}:{secs:02d}", end='', flush=True)
        time.sleep(0.2)

    print("\r  残り 00:00 → キャプチャ開始！\n")


# ===== Webカメラキャプチャ =====
def capture_frame():
    """Webカメラから1フレームキャプチャして screenshots/ に保存"""
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    print(f"[カメラ起動] デバイス {CAMERA_INDEX} に接続中...")
    warmup_end = time.time() + CAMERA_WARMUP
    while time.time() < warmup_end:
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("[ERROR] カメラからの取得に失敗しました")
        return None

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"auto_{timestamp}.png"
    path      = os.path.join(SCREENSHOT_DIR, filename)
    cv2.imwrite(path, frame)

    print(f"[キャプチャ完了] {filename}  ({frame.shape[1]}x{frame.shape[0]})")
    return path


# ===== フレーム誤差表示 =====
def print_frame_diff(result, target_frame):
    # TARGET_FRAME周辺のみ検索して処理を軽くする
    search_start = max(0, target_frame - SEARCH_MARGIN)
    search_end   = target_frame + SEARCH_MARGIN
    frames = find_frame(
        result['skill1_name'], result['skill1_val'],
        result['skill2_name'], result['skill2_val'],
        result['slots'],
        start_frame=search_start,
        max_frame=search_end
    )

    print("\n===== フレーム誤差 =====")
    if not frames:
        print("  読み取った護石のフレームが見つかりませんでした")
        print("  （OCR誤認識の可能性があります）")
        return

    closest  = min(frames, key=lambda x: abs(x - target_frame))
    diff     = closest - target_frame
    diff_ms  = int(diff / 30 * 1000)
    sign     = '+' if diff >= 0 else ''

    print(f"  ターゲット : {target_frame:,} F")
    print(f"  最近傍    : {closest:,} F")
    print(f"  誤差      : {sign}{diff:,} F  ({sign}{diff_ms} ms)")

    if diff == 0:
        print("  ★ ピッタリ！")
    elif abs(diff) <= 30:
        print("  ○ 1秒以内の誤差")
    else:
        print("  △ Arduino の ADJUST_F を更新してください")
        adj_suggestion = diff  # ADJUST_F += diff で補正
        print(f"    → ADJUST_F の調整値: {sign}{adj_suggestion} F")

    print("========================\n")


# ===== メイン =====
def main():
    # --- 引数チェック ---
    if len(sys.argv) < 2:
        print("使い方: python auto_capture.py <待機秒数>")
        print("  例)  python auto_capture.py 320")
        sys.exit(1)

    try:
        wait_seconds = int(sys.argv[1])
        if wait_seconds < 0:
            raise ValueError
    except ValueError:
        print("[ERROR] 待機秒数は0以上の整数で指定してください")
        sys.exit(1)

    print(f"[ターゲット] {TARGET_FRAME:,} F  (検索範囲 ±{SEARCH_MARGIN:,}F)\n")

    # --- スリープ防止（待機中にPCが止まらないように）---
    _sleep_prevent()

    # --- 待機 ---
    if WAIT_MODE == 'time':
        if wait_seconds > 0:
            countdown(wait_seconds)
        else:
            print("[待機スキップ] 即時キャプチャします\n")

    # （フェーズ2用プレースホルダー）
    # elif WAIT_MODE == 'serial':
    #     wait_for_serial_done(SERIAL_PORT, SERIAL_BAUD)

    # --- キャプチャ ---
    image_path = capture_frame()
    if image_path is None:
        sys.exit(1)

    # --- OCR ---
    result = read_talisman(image_path)
    if not result:
        print("[ERROR] 護石の読み取りに失敗しました")
        sys.exit(1)

    print_result(result)
    save_to_csv(result)

    # --- フレーム誤差 ---
    print_frame_diff(result, TARGET_FRAME)

    # --- スリープ防止を解除 ---
    _sleep_allow()


if __name__ == "__main__":
    main()

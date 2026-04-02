"""
serial_auto.py - Arduino シリアル通信による完全自動化

auto_capture.py との違い:
  - 時間待ちではなくArduinoから "DONE" を受信したらキャプチャ
  - PCから "TARGET:N" でターゲットフレームをArduinoへ送信（スケッチ書き換え不要）
  - PCから "START" を送信してArduinoのマクロを起動
  - adjust_f に応じて "ADJUST:±N" を送信し、Arduinoが自動で再実行
  - 最大 MAX_LOOPS 回まで自動ループ
  - 各ループの結果を serial_auto_log.csv に記録

【使い方】
  python capture/serial_auto.py
  ※ 事前に SERIAL_PORT と TARGET_FRAME を設定すること

【フロー】
  1. COMポートを開いてArduinoが "READY" を送信するまで待機
  2. "TARGET:N" を送信 → "OK" を受信（ターゲットフレーム設定）
  3. "START" を送信 → Arduinoがマクロを起動
  4. "DONE" を受信 → Webカメラキャプチャ → OCR → フレーム誤差算出 → CSV記録
  5. adjust_f == 0 → 終了（成功）
  6. ループ回数が MAX_LOOPS に達した → 終了（上限到達）
  7. "ADJUST:±N" を送信 → "ACK" を受信 → 3へ戻る

【シリアル通信コマンド（Arduinoと対応）】
  PC → Arduino:
    TARGET:N    ターゲットフレームを設定（READY受信後に送る）
    START       マクロ起動
    ADJUST:+N   ADJUST_F に +N を加算して再実行
    ADJUST:-N   ADJUST_F に -N を加算して再実行
    STOP        処理終了
  Arduino → PC:
    READY       起動完了・コマンド待機中
    OK          TARGET受信・calcParams完了
    DONE        マクロ完了通知
    ACK         ADJUST受信・再実行開始

【依存ライブラリ】
  pyserial が必要:  pip install pyserial
"""

import csv
import cv2
import sys
import os
import time
import ctypes
import serial
from datetime import datetime

# ===== Windows スリープ防止 =====
_ES_CONTINUOUS       = 0x80000000
_ES_SYSTEM_REQUIRED  = 0x00000001
_ES_DISPLAY_REQUIRED = 0x00000002

def _sleep_prevent():
    ctypes.windll.kernel32.SetThreadExecutionState(
        _ES_CONTINUOUS | _ES_SYSTEM_REQUIRED | _ES_DISPLAY_REQUIRED
    )

def _sleep_allow():
    ctypes.windll.kernel32.SetThreadExecutionState(_ES_CONTINUOUS)

# =========================================
#   ★ 設定（環境に合わせて変更する）
# =========================================

# シリアルポート設定
# デバイスマネージャーで「ポート(COMとLPT)」を確認してCOM番号を調べる
SERIAL_PORT = 'COM12'   # ★ USB-シリアル変換器のCOMポートに変更する
SERIAL_BAUD = 9600

# タイムアウト設定（秒）
TIMEOUT_READY  = 30     # READY受信タイムアウト（Arduino起動後）
TIMEOUT_DONE   = 9000   # DONE受信タイムアウト（マクロ実行中、秒）= 150分
TIMEOUT_ACK    = 30     # ACK受信タイムアウト（ADJUST送信後）

# ループ上限
MAX_LOOPS = 4

# ===== ターゲットフレーム設定 =====
# ★ 護石を変えるときにここだけ変更する（Arduinoスケッチの書き換えは不要）
TARGET_FRAME = 702223

# OCR後のフレーム検索範囲: TARGET_FRAME ± SEARCH_MARGIN
SEARCH_MARGIN = 100000

# ===== カメラ設定 =====
CAMERA_INDEX  = 0
CAMERA_WIDTH  = 1920
CAMERA_HEIGHT = 1080
CAMERA_WARMUP = 1.0     # カメラ起動後の安定待機（秒）

# ===== パス設定 =====
_BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(_BASE_DIR, 'screenshots')
SERIAL_LOG_CSV = os.path.join(_BASE_DIR, 'serial_auto_log.csv')

sys.path.insert(0, _BASE_DIR)
from read_talisman import read_talisman, print_result, save_to_csv
from find_frame import find_frame


# =========================================
#   実行ログ CSV 保存
# =========================================

_LOG_FIELDS = [
    'timestamp', 'loop', 'target_frame',
    'skill1_name', 'skill1_val', 'skill2_name', 'skill2_val', 'slots',
    'closest_frame', 'adjust_f', 'status',
]

def save_run_log(loop, ocr_result, closest_frame, adjust_f, status):
    """
    1ループ分の実行結果を serial_auto_log.csv に追記する。

    status の値:
      success       adjust_f == 0（成功）
      continuing    次のループへ進む
      ocr_failed    OCRでフレームが見つからなかった
      limit_reached MAX_LOOPS に達した
      error         キャプチャ失敗・通信エラーなど
    """
    file_exists = os.path.exists(SERIAL_LOG_CSV)
    row = {
        'timestamp':    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'loop':         loop,
        'target_frame': TARGET_FRAME,
        'skill1_name':  ocr_result['skill1_name'] if ocr_result else '',
        'skill1_val':   ocr_result['skill1_val']  if ocr_result else '',
        'skill2_name':  ocr_result['skill2_name'] if ocr_result else '',
        'skill2_val':   ocr_result['skill2_val']  if ocr_result else '',
        'slots':        ocr_result['slots']        if ocr_result else '',
        'closest_frame': closest_frame if closest_frame is not None else '',
        'adjust_f':     adjust_f       if adjust_f      is not None else '',
        'status':       status,
    }
    with open(SERIAL_LOG_CSV, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=_LOG_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"[CSV記録] {SERIAL_LOG_CSV}  status={status}")


# =========================================
#   シリアル通信ヘルパー
# =========================================

def serial_send(ser, message):
    """Arduinoへコマンドを送信する"""
    ser.write((message + '\n').encode('utf-8'))
    print(f"  [送信] {message}")


def serial_wait_for(ser, expected, timeout_sec):
    """
    expected で始まる行を受信するまでブロッキング待機。
    timeout_sec 秒以内に受信できなければ None を返す。
    """
    deadline = time.time() + timeout_sec
    buffer = ""
    while time.time() < deadline:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            buffer += chunk
            lines = buffer.split('\n')
            buffer = lines[-1]  # 最後の不完全行をバッファに残す
            for line in lines[:-1]:
                line = line.strip()
                if not line:
                    continue
                print(f"  [受信] {line}")
                if line.startswith(expected):
                    return line
        time.sleep(0.05)
    print(f"  [タイムアウト] {expected} を {timeout_sec}秒以内に受信できませんでした")
    return None


# =========================================
#   Webカメラキャプチャ
# =========================================

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
    filename  = f"serial_{timestamp}.png"
    path      = os.path.join(SCREENSHOT_DIR, filename)
    cv2.imwrite(path, frame)

    print(f"[キャプチャ完了] {filename}  ({frame.shape[1]}x{frame.shape[0]})")
    return path


# =========================================
#   フレーム誤差計算
#   戻り値: (adjust_f, closest_frame)
#     adjust_f     : int（フレーム単位）、護石が見つからない場合は None
#     closest_frame: 最近傍フレーム番号、見つからない場合は None
# =========================================

def calc_adjust_f(result, target_frame):
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
        print("========================\n")
        return None, None

    closest = min(frames, key=lambda x: abs(x - target_frame))
    diff    = closest - target_frame
    sign    = '+' if diff >= 0 else ''

    print(f"  ターゲット : {target_frame:,} F")
    print(f"  最近傍    : {closest:,} F")
    print(f"  誤差      : {sign}{diff:,} F")

    if diff == 0:
        print("  ★ ピッタリ！ → 終了します")
    elif abs(diff) <= 30:
        print("  ○ 1秒以内の誤差 → 終了します")
        diff = 0  # 許容範囲内なら調整不要とみなす
    else:
        print(f"  △ ADJUST_F を {sign}{diff} F 調整します")

    print("========================\n")
    return diff, closest


# =========================================
#   メイン
# =========================================

def main():
    print("=" * 50)
    print("  MHXX 護石スナイプ 完全自動化モード")
    print("=" * 50)
    print(f"  シリアルポート : {SERIAL_PORT}  ({SERIAL_BAUD} baud)")
    print(f"  ターゲット     : {TARGET_FRAME:,} F")
    print(f"  最大ループ数   : {MAX_LOOPS} 回")
    print("=" * 50 + "\n")

    _sleep_prevent()

    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
    except serial.SerialException as e:
        print(f"[ERROR] シリアルポートを開けませんでした: {e}")
        print(f"  → デバイスマネージャーでCOM番号を確認し、SERIAL_PORT を変更してください")
        _sleep_allow()
        sys.exit(1)

    print(f"[接続] {SERIAL_PORT} を開きました\n")

    # Arduino は接続直後にリセットされることがあるので少し待つ
    time.sleep(2)
    ser.reset_input_buffer()

    # READY 待機
    print("[待機] Arduino の起動完了 (READY) を待っています...")
    ready = serial_wait_for(ser, "READY", TIMEOUT_READY)
    if ready is None:
        print("[ERROR] Arduino からの READY を受信できませんでした")
        print("  → Arduinoがmhxx-rng-serial.inoを書き込んだLeonardoか確認してください")
        ser.close()
        _sleep_allow()
        sys.exit(1)

    # TARGET 送信（スケッチを書き換えなくてもターゲットフレームをArduinoへ設定）
    print(f"\n[送信] ターゲットフレームを送信します: {TARGET_FRAME:,} F")
    serial_send(ser, f"TARGET:{TARGET_FRAME}")
    ok = serial_wait_for(ser, "OK", TIMEOUT_ACK)
    if ok is None:
        print("[ERROR] OK を受信できませんでした。TARGET コマンドに失敗しました。")
        ser.close()
        _sleep_allow()
        sys.exit(1)
    print()

    # =========================================
    #   メインループ
    # =========================================
    for loop_count in range(1, MAX_LOOPS + 1):
        print(f"{'='*50}")
        print(f"  ループ {loop_count} / {MAX_LOOPS}")
        print(f"{'='*50}\n")

        # --- START 送信 ---
        print("[送信] Arduinoにマクロ起動を指示します...")
        serial_send(ser, "START")
        print()

        # --- DONE 受信待機 ---
        print(f"[待機] マクロ完了 (DONE) を待っています... （最大 {TIMEOUT_DONE//60} 分）")
        done = serial_wait_for(ser, "DONE", TIMEOUT_DONE)
        if done is None:
            print("[ERROR] DONE を受信できませんでした。処理を中断します。")
            serial_send(ser, "STOP")
            save_run_log(loop_count, None, None, None, 'error')
            break
        print()

        # --- キャプチャ ---
        image_path = capture_frame()
        if image_path is None:
            print("[ERROR] カメラキャプチャに失敗しました。処理を中断します。")
            serial_send(ser, "STOP")
            save_run_log(loop_count, None, None, None, 'error')
            break

        # --- OCR ---
        result = read_talisman(image_path)
        if not result:
            print("[ERROR] 護石の読み取りに失敗しました。処理を中断します。")
            serial_send(ser, "STOP")
            save_run_log(loop_count, None, None, None, 'error')
            break
        print_result(result)
        save_to_csv(result)

        # --- フレーム誤差計算 ---
        adjust_f, closest_frame = calc_adjust_f(result, TARGET_FRAME)

        if adjust_f is None:
            print("[WARN] フレームが見つかりませんでした。処理を中断します。")
            serial_send(ser, "STOP")
            save_run_log(loop_count, result, None, None, 'ocr_failed')
            break

        if adjust_f == 0:
            # 成功 → 終了
            print("[完了] adjust_f = 0 → プログラムを終了します。\n")
            serial_send(ser, "STOP")
            save_run_log(loop_count, result, closest_frame, adjust_f, 'success')
            break

        if loop_count >= MAX_LOOPS:
            # 上限到達 → 終了
            print(f"[終了] {MAX_LOOPS} 回ループしても adjust_f ≠ 0 → プログラムを終了します。\n")
            serial_send(ser, "STOP")
            save_run_log(loop_count, result, closest_frame, adjust_f, 'limit_reached')
            break

        # CSV記録（次のループへ継続）
        save_run_log(loop_count, result, closest_frame, adjust_f, 'continuing')

        # --- ADJUST 送信 ---
        sign = '+' if adjust_f >= 0 else ''
        cmd  = f"ADJUST:{sign}{adjust_f}"
        print(f"[送信] Arduino へ調整値を送信します: {cmd}")
        serial_send(ser, cmd)

        # --- ACK 受信待機 ---
        print(f"[待機] ACK を待っています...")
        ack = serial_wait_for(ser, "ACK", TIMEOUT_ACK)
        if ack is None:
            print("[ERROR] ACK を受信できませんでした。処理を中断します。")
            break
        print(f"[受信確認] Arduinoがゲームを再起動してマクロを再実行します\n")

    # =========================================
    #   終了処理
    # =========================================
    ser.close()
    _sleep_allow()
    print("[終了] シリアルポートを閉じました。")


if __name__ == "__main__":
    main()
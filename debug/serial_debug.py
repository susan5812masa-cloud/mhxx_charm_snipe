# =============================================================
# serial_debug.py
# PC-Arduino シリアル通信デバッグ用スクリプト
#
# 接続: PC - CH340(TX/RX) - Arduino
#
# 必要ライブラリ:
#   pip install pyserial
#
# 実行方法（VS Code ターミナル または cmd）:
#   python debug\serial_debug.py
#
# 動作フロー:
#   1. PC → Arduino: "start" 送信
#   2. Arduino からの "done" を待機
#   3. PC → Arduino: "end" 送信
#   4. Arduino が赤LED点灯→消灯し待機状態へ
# =============================================================

import serial
import time

# =============================================================
# ★ 設定（環境に合わせて書き換えてください）
# =============================================================
COM_PORT  = "COM12"   # CH340が割り当てられたCOMポート番号
BAUD_RATE = 9600     # ボーレート（serial_debug.inoと合わせること）
TIMEOUT   = 30       # "done" 待機タイムアウト（秒）
# =============================================================


def open_serial(port: str, baud: int) -> serial.Serial | None:
    """シリアルポートを開く。失敗時はNoneを返す。"""
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print(f"[INFO] ポート {port} をオープンしました（{baud}bps）")
        return ser
    except serial.SerialException as e:
        print(f"[ERROR] ポートを開けませんでした: {e}")
        print(f"        デバイスマネージャーでCOMポート番号を確認し、")
        print(f"        スクリプト上部の COM_PORT を書き換えてください。")
        return None


def wait_for_response(ser: serial.Serial, expected: str, timeout_sec: int) -> bool:
    """
    Arduinoからの応答を待つ。
    expected: 期待する文字列（例: "done"）
    timeout_sec: タイムアウト秒数
    戻り値: 受信成功でTrue、タイムアウトでFalse
    """
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8", errors="replace").strip()
            if line:
                print(f"[RECV] {line}")
            if line == expected:
                return True
    return False


def main():
    print("=" * 50)
    print("  Arduino シリアル通信デバッグ")
    print("=" * 50)

    # --- シリアルポートを開く ---
    ser = open_serial(COM_PORT, BAUD_RATE)
    if ser is None:
        return

    # CH340経由でポートを開くとArduinoがリセットされる場合があるため待機
    print("[INFO] Arduino の起動待ち（2秒）...")
    time.sleep(2)
    ser.reset_input_buffer()

    # 起動時のArduinoメッセージを読み捨て（あれば表示）
    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if line:
            print(f"[RECV] {line}")

    # --- 1. "start" 送信 ---
    print("[INFO] 'start' を送信します...")
    ser.write(b"start\n")

    # --- 2. "done" を待機 ---
    print(f"[INFO] Arduino からの 'done' を待機中...（タイムアウト: {TIMEOUT}秒）")
    if not wait_for_response(ser, "done", TIMEOUT):
        print("[ERROR] タイムアウト: 'done' を受信できませんでした。")
        print("        Arduinoの接続・スケッチを確認してください。")
        ser.close()
        return

    print("[INFO] 'done' を受信しました。")

    # --- 3. "end" 送信 ---
    print("[INFO] 'end' を送信します...")
    ser.write(b"end\n")
    print("[INFO] 送信完了。")
    print("[INFO] Arduino は赤LEDを5秒間点灯後、待機状態（READY）に戻ります。")

    # --- 後続のArduinoメッセージを少し受け取る（任意）---
    time.sleep(0.5)
    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if line:
            print(f"[RECV] {line}")

    # --- 終了 ---
    ser.close()
    print("[INFO] ポートをクローズしました。")
    print("=" * 50)
    print("  デバッグ完了")
    print("=" * 50)


if __name__ == "__main__":
    main()

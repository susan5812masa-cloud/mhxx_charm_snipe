// =============================================================
// serial_debug.ino
// PC-Arduino シリアル通信デバッグ用スケッチ
//
// 接続: PC - CH340(TX/RX) - Arduino
//   CH340 TX  →  Arduino Pin0 (RX)
//   CH340 RX  →  Arduino Pin1 (TX)
//   ※ スケッチ書き込み時はCH340のTX/RXを外してください
//
// 動作フロー:
//   1. PC → Arduino: "start\n"
//   2. Arduino: 緑LED 500ms間隔で5回点滅
//   3. Arduino → PC: "done\n"
//   4. PC → Arduino: "end\n"
//   5. Arduino: 赤LED 5秒点灯 → 消灯 → READY状態へ戻る
// =============================================================

// --- ピン設定（CLAUDE.mdの既存定義に合わせる）---
const int PIN_GREEN_LED = 3;
const int PIN_RED_LED   = 4;

// --- 通信設定 ---
const long BAUD_RATE = 9600;

// --- 点滅パラメータ ---
const int    BLINK_COUNT    = 5;
const int    BLINK_INTERVAL = 500;  // ms (ON/OFFそれぞれ)

// --- 赤LED点灯時間 ---
const int RED_ON_DURATION = 5000;  // ms

// --- 状態定義 ---
enum State {
  READY,        // PCからの "start" 待機中
  RUNNING,      // 緑LED点滅実行中
  WAITING_END   // PCからの "end" 待機中
};

State currentState = READY;

// =============================================================
void setup() {
  Serial1.begin(BAUD_RATE);  // Leonardo: Serial1 = D0/D1(TX/RX)

  pinMode(PIN_GREEN_LED, OUTPUT);
  pinMode(PIN_RED_LED,   OUTPUT);
  digitalWrite(PIN_GREEN_LED, LOW);
  digitalWrite(PIN_RED_LED,   LOW);

  // 起動メッセージ
  Serial1.println("[ARDUINO] Ready. Waiting for 'start'...");
}

// =============================================================
void loop() {

  // --- READY: "start" を待つ ---
  if (currentState == READY) {
    if (Serial1.available() > 0) {
      String cmd = Serial1.readStringUntil('\n');
      cmd.trim();

      if (cmd == "start") {
        Serial1.println("[ARDUINO] Received 'start'. Blinking green LED...");
        currentState = RUNNING;

        // 緑LED 5回点滅
        for (int i = 0; i < BLINK_COUNT; i++) {
          digitalWrite(PIN_GREEN_LED, HIGH);
          delay(BLINK_INTERVAL);
          digitalWrite(PIN_GREEN_LED, LOW);
          delay(BLINK_INTERVAL);
        }

        // 完了通知
        Serial1.println("done");
        Serial1.println("[ARDUINO] Blink done. Waiting for 'end'...");
        currentState = WAITING_END;
      }
    }

  // --- WAITING_END: "end" を待つ ---
  } else if (currentState == WAITING_END) {
    if (Serial1.available() > 0) {
      String cmd = Serial1.readStringUntil('\n');
      cmd.trim();

      if (cmd == "end") {
        Serial1.println("[ARDUINO] Received 'end'. Red LED ON for 5s...");
        digitalWrite(PIN_RED_LED, HIGH);
        delay(RED_ON_DURATION);
        digitalWrite(PIN_RED_LED, LOW);

        Serial1.println("[ARDUINO] Ready. Waiting for 'start'...");
        currentState = READY;
      }
    }
  }
}

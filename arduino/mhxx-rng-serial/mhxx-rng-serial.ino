#include <NintendoSwitchControlLibrary.h>

// =========================================
// ★☆★ PC-Arduino シリアル通信 完全自動化版 ★☆★
//
//   手動版 (mhxx-rng-long.ino) との違い:
//   - TARGET_FRAME と ADJUST_F が const ではなく書き換え可能な変数
//   - Serial1 (ピン0=RX, 1=TX) でPCと通信
//   - PCからの "TARGET:N" でターゲットフレームを設定
//   - PCからの "START" でもマクロ起動可能
//   - マクロ完了後 "DONE" をPCへ送信
//   - PCからの "ADJUST:±N" で ADJUST_F を更新して自動再実行
//   - 物理ボタンによる手動起動も引き続き使用可能
//
//   【シリアル通信コマンド一覧】
//   PC → Arduino:
//     TARGET:N    ターゲットフレームを設定（READY受信後に送る）
//     START       マクロ起動（自動モード）
//     ADJUST:+N   ADJUST_F に +N を加算して再実行
//     ADJUST:-N   ADJUST_F に -N を加算して再実行
//     STOP        処理を終了する
//   Arduino → PC:
//     READY       起動完了・コマンド待機中
//     OK          TARGET受信・calcParams完了
//     DONE        マクロ完了通知
//     ACK         ADJUST受信・再実行開始
// =========================================

// =========================================
//   ターゲットフレーム（PCからの TARGET コマンドで上書きされる）
//   ★ 手動モード（ボタン起動）では、この初期値が使われる
// =========================================
unsigned long TARGET_FRAME = 702223;

// =========================================
//   ★ キャリブレーション（実測のたびに更新する）
//
//   ADJUST_F = 実測F - 目標F
//   例) 目標296260F → 実測303260F のとき
//       ADJUST_F = 303260 - 296260 = 7000
//
//   ※ 自動モードではPCからの ADJUST コマンドで上書きされる
//   ※ 対応範囲: -2000F < ADJUST_F < +15000F
// =========================================
float ADJUST_F = -521.0f;  // ← const を外して書き換え可能に

// =========================================
//   ★ 環境定数（再測定したときだけ更新する）
// =========================================
const float         FC          = 725.71f;
const float         F_BEFORE_MS =   0.02797f;
const float         F_AFTER_MS  =   0.032535f;
const float         BASE_CONST  = 1750.475f;  // ★この値は変更しない
const unsigned long WAIT_BEFORE = 20000UL;    // 事前待機(ms)

// =========================================
//   調整範囲の制限
// =========================================
const unsigned long T2_MIN    =    1000UL;
const unsigned long T2_MAX    =  600000UL;
const int           NC_MARGIN =       20;

// =========================================
//   タイムアウト設定
// =========================================
const unsigned long TIMEOUT_MS       = 10000UL;   // 手動モード完了後の停止までの時間(ms)
const unsigned long WAIT_ADJUST_TIMEOUT = 600000UL; // ADJUST待機タイムアウト(ms) = 10分

// =========================================
//   シリアル設定
// =========================================
const long SERIAL1_BAUD = 9600;  // USB-シリアル変換器との通信速度

// =========================================
//   自動計算結果（変更不要）
// =========================================
unsigned long NUM_CONTINUE = 0;
unsigned long WAIT_AFTER   = 0;

// =========================================
//   ピン定義
// =========================================
const int PIN_BUTTON = 2;
const int PIN_LED1   = 3;  // 緑（実行中）
const int PIN_LED2   = 4;  // 赤（完了 / ADJUST待機中）

// =========================================
//   状態管理
// =========================================
enum State { WAITING, RUNNING, WAIT_ADJUST, DONE, STOPPED };
State state      = WAITING;
bool  serialMode = false;  // true=PCからのSTARTで起動 / false=ボタンで起動

// =========================================
//   自動計算関数
// =========================================
void calcParams() {
  float fixed_nominal  = F_BEFORE_MS * WAIT_BEFORE + BASE_CONST;
  float nc_max_f       = (TARGET_FRAME - fixed_nominal - F_AFTER_MS * T2_MIN) / FC;
  long  nc             = (nc_max_f > 0) ? (long)nc_max_f - NC_MARGIN : 0L;
  NUM_CONTINUE         = (nc > 0) ? (unsigned long)nc : 0UL;

  float fixed_adjusted = fixed_nominal + ADJUST_F;
  float t2             = (TARGET_FRAME - FC * NUM_CONTINUE - fixed_adjusted) / F_AFTER_MS;

  if (t2 < (float)T2_MIN) t2 = (float)T2_MIN;
  if (t2 > (float)T2_MAX) t2 = (float)T2_MAX;

  WAIT_AFTER = (unsigned long)t2;
}

// =========================================
//   長時間待機（5秒ごとにXボタンで接続維持）
// =========================================
void waitKeepAlive(unsigned long total_ms) {
  if (total_ms <= 10000) {
    delay(total_ms);
    return;
  }
  const unsigned long INTERVAL = 5000;
  const unsigned long PRESS    =  100;
  unsigned long n   = total_ms / INTERVAL;
  unsigned long rem = total_ms % INTERVAL;
  for (unsigned long i = 0; i < n; i++) {
    pushButton(Button::X, PRESS);
    delay(INTERVAL - PRESS);
  }
  if (rem > 0) delay(rem);
}

// =========================================
//   シリアル1行読み取り（ブロッキング・タイムアウト付き）
//   待機中も sendReport() を呼んで Switch 接続を維持する
// =========================================
String readSerialLine(unsigned long timeout_ms) {
  String line = "";
  unsigned long start = millis();
  while (millis() - start < timeout_ms) {
    while (Serial1.available()) {
      char c = (char)Serial1.read();
      if (c == '\n') {
        line.trim();
        return line;
      }
      if (c != '\r') line += c;
    }
    SwitchControlLibrary().sendReport();
    delay(10);
  }
  line.trim();
  return line;  // タイムアウト時は空文字 or 途中の文字列を返す
}

// =========================================
//   ゲーム再起動（自動モードでADJUST後に呼ぶ）
//
//   ※ マクロ終了後はゲームが村エリア（護石鑑定確認画面）で停止している
//   ※ HOMEボタンでメニューへ → ソフト終了 → 再起動
//   ★ Switchのホーム画面の表示速度により delay を調整が必要な場合がある
// =========================================
void restartGame() {
  // ホームメニューへ戻る
  pushButton(Button::HOME, 250);
  delay(2000);  // ★ ホームメニュー表示待機（遅い場合は増やす）

  // ソフトを終了
  pushButton(Button::X, 250);    // 「ソフトを終了しますか？」ダイアログ
  delay(500);
  pushButton(Button::A, 250);    // 終了を確定
  delay(3000);  // ★ ソフト終了・ホームメニューに戻るまでの待機

  // ゲームを再起動（直前に起動していたためカーソルはゲームに当たっている）
  pushButton(Button::A, 250);
  delay(2000);  // ★ 起動アニメーション待機（長い場合は増やす）
}

// =========================================
//   メインマクロ
// =========================================
void runMacro() {

  // ① ゲーム起動 → ゲームモード選択画面まで A連打
  pushButton(Button::A, 250, 32);

// =========================================
  //↓2行を入れる場合は↑を32に、↓を消す場合は↑を34に
  delay(750);
  pushButton(Button::A, 250);
// =========================================

  // ② 事前待機
  waitKeepAlive(WAIT_BEFORE);

  // ③ continue連打（A→B × NUM_CONTINUE回）
  for (unsigned long i = 0; i < NUM_CONTINUE; i++) {
    pushButton(Button::A, 100);
    delay(100);
    pushButton(Button::B, 100);
    delay(100);
  }
  pushButton(Button::A, 100);
  delay(100);

  // ④ 事後待機
  waitKeepAlive(WAIT_AFTER);

  // ⑤ Continue選択 → キャラクター選択まで A連打
  pushButton(Button::A, 250, 4);

  // ⑥ ゲームロード待機
  delay(10000);

  // ⑦ マカ錬金屋へ左上ダッシュ（Rを押しながら）
  tiltLeftStick(100, 0, 3700, Button::R);
  delay(100);

  // ⑧ マカ錬金屋に話しかけ → 護石投入
  pushButton(Button::A, 100);
  pushButton(Button::B, 250, 6);
  pushButton(Button::A, 100);
  pushHat(Hat::UP);
  pushButton(Button::A, 10);
  pushButton(Button::A, 10);
  pushHat(Hat::DOWN, 10);
  pushButton(Button::A, 10);
  pushHat(Hat::DOWN, 10);
  pushButton(Button::A, 10);
  pushButton(Button::A, 100, 2);
  pushButton(Button::B, 100, 5);

  // ⑨ 受付嬢へ右上ダッシュ（Rを押しながら）
  tiltLeftStick(255, 0, 1700, Button::R);
  delay(100);

  // ⑩ ケルビクエスト受注
  pushButton(Button::A, 250, 3);
  pushButton(Button::B, 250, 4);
  delay(100);
  pushHat(Hat::UP);
  pushButton(Button::A, 100);
  pushHat(Hat::DOWN);
  pushButton(Button::A, 100);
  pushHat(Hat::DOWN, 50, 3);
  pushButton(Button::A, 50, 5);
  pushButton(Button::B, 250, 4);

  // ⑪ 門へ移動してクエスト出発（Rを押しながら）
  tiltLeftStick(0, 128, 800, Button::R);
  tiltLeftStick(128, 0, 2300, Button::R);
  delay(100);
  pushButton(Button::A, 50, 5);

  // ⑫ クエスト開始待機
  delay(8700);

  // ⑬ メニューを開いてケルビの角を納品
  pushButton(Button::PLUS, 250);
  pushButton(Button::A, 250, 2);
  pushHat(Hat::DOWN, 50, 2);
  pushButton(Button::A, 250);
  pushHat(Hat::RIGHT);
  pushButton(Button::A, 250, 4);

  // ⑭ クエスト終了まで待機
  delay(36000);

  // ⑮ 報酬売却（セーブしない）
  pushHat(Hat::UP);
  pushButton(Button::A, 250);
  pushHat(Hat::LEFT);
  pushButton(Button::A, 250, 5);
  pushButton(Button::B, 250);
  pushButton(Button::A, 250);

  // ⑯ 帰還まで待機
  delay(7900);

  // ⑰ 自宅へ移動
  pushButton(Button::X, 250);
  pushButton(Button::A, 250, 2);

  // ⑱ 鑑定確認画面で停止
  delay(2000);
  tiltLeftStick(255, 128, 700);
  pushButton(Button::A, 250, 2);
  pushButton(Button::B, 250, 2);
  delay(100);
  pushButton(Button::A, 250);
  pushHat(Hat::DOWN, 50, 3);
  pushButton(Button::A, 250);
  pushHat(Hat::DOWN, 50);
  pushButton(Button::A, 250, 2);
  delay(1500);
  pushButton(Button::A, 250);
}

// =========================================
//   setup / loop
// =========================================
void setup() {
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_LED1, OUTPUT);
  pinMode(PIN_LED2, OUTPUT);

  // シリアル通信初期化（USB-シリアル変換器との通信）
  Serial1.begin(SERIAL1_BAUD);

  // パラメータ自動計算
  calcParams();

  // Switch認識用
  pushButton(Button::B, 500, 5);

  // 起動確認：緑LED3回点滅
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_LED1, HIGH);
    delay(200);
    digitalWrite(PIN_LED1, LOW);
    delay(200);
  }

  // PCへ起動完了通知
  Serial1.println("READY");
}

void loop() {

  // -----------------------------------------
  //   WAITING: ボタンまたはPCからの START を待機
  // -----------------------------------------
  if (state == WAITING) {
    SwitchControlLibrary().sendReport();
    delay(100);

    // 物理ボタン（手動モード）
    if (digitalRead(PIN_BUTTON) == LOW) {
      delay(50);  // チャタリング防止
      serialMode = false;
      state = RUNNING;
    }

    // PCからのコマンド（自動モード）
    if (Serial1.available()) {
      String cmd = readSerialLine(1000);
      if (cmd.startsWith("TARGET:")) {
        // ターゲットフレームを更新してパラメータ再計算
        TARGET_FRAME = strtoul(cmd.substring(7).c_str(), nullptr, 10);
        calcParams();
        Serial1.println("OK");
      } else if (cmd == "START") {
        serialMode = true;
        state = RUNNING;
      }
    }
  }

  // -----------------------------------------
  //   RUNNING: マクロ実行
  // -----------------------------------------
  if (state == RUNNING) {
    digitalWrite(PIN_LED1, HIGH);
    runMacro();
    digitalWrite(PIN_LED1, LOW);

    if (serialMode) {
      // 自動モード: PCへ完了通知 → ADJUST待機へ
      Serial1.println("DONE");
      digitalWrite(PIN_LED2, HIGH);
      state = WAIT_ADJUST;
    } else {
      // 手動モード: 元の動作（タイムアウト後に停止）
      state = DONE;
    }
  }

  // -----------------------------------------
  //   WAIT_ADJUST: PCから ADJUST または STOP を待機
  //   （自動モード専用）
  // -----------------------------------------
  if (state == WAIT_ADJUST) {
    String cmd = readSerialLine(WAIT_ADJUST_TIMEOUT);

    if (cmd.startsWith("ADJUST:")) {
      // ADJUST_F を加算更新してパラメータ再計算
      float delta = cmd.substring(7).toFloat();
      ADJUST_F += delta;
      calcParams();

      Serial1.println("ACK");
      digitalWrite(PIN_LED2, LOW);

      // ゲームを再起動してマクロを再実行
      restartGame();
      state = RUNNING;

    } else {
      // STOP または タイムアウト → 終了
      digitalWrite(PIN_LED2, LOW);
      state = STOPPED;
    }
  }

  // -----------------------------------------
  //   DONE: 手動モード完了（タイムアウト後に停止）
  // -----------------------------------------
  if (state == DONE) {
    digitalWrite(PIN_LED2, HIGH);
    unsigned long n   = TIMEOUT_MS / 100;
    unsigned long rem = TIMEOUT_MS % 100;
    for (unsigned long i = 0; i < n; i++) {
      SwitchControlLibrary().sendReport();
      delay(100);
    }
    if (rem > 0) delay(rem);

    digitalWrite(PIN_LED2, LOW);
    state = STOPPED;
  }

  // -----------------------------------------
  //   STOPPED: 完全停止（リセットまたは抜き差しで再起動）
  // -----------------------------------------
  if (state == STOPPED) {
    while (true) {}
  }
}

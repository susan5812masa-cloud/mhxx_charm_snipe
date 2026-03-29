#include <NintendoSwitchControlLibrary.h>

// =========================================
// ★☆★ターゲットフレームが大きい時用のコード★☆★
//   ★ ターゲットフレーム（護石を変えるときに変更する）
// =========================================
const unsigned long TARGET_FRAME = 702223;  //

// =========================================
//   ★ キャリブレーション（実測のたびに更新する）
//
//   ADJUST_F = 実測F - 目標F
//   例) 目標296260F → 実測303260F のとき
//       ADJUST_F = 303260 - 296260 = 7000
//
//   ※ Nc は変わらず WAIT_AFTER だけで誤差を吸収する
//   ※ 対応範囲: -2000F < ADJUST_F < +15000F
// =========================================
const float ADJUST_F = -521.0f;

// =========================================
//   ★ 環境定数（再測定したときだけ更新する）
//
//   FC           : continue1回あたりのF消費（実測平均）
//   F_BEFORE_MS  : WAIT_BEFORE 1msあたりのF消費（実測値）
//   F_AFTER_MS   : WAIT_AFTER  1msあたりのF消費（実測値）
//   BASE_CONST   : 固定消費F（起動・ロード・操作等の固定分）★変更しない
//   WAIT_BEFORE  : continue連打前の事前待機(ms)　固定値
// =========================================
const float         FC          = 725.71f;
const float         F_BEFORE_MS =   0.02797f;
const float         F_AFTER_MS  =   0.032535f;
const float         BASE_CONST  = 1750.475f;  // ★この値は変更しない
const unsigned long WAIT_BEFORE = 20000UL;    // 事前待機(ms)

// =========================================
//   調整範囲の制限
//   NC_MARGIN=20 により -2000F〜+15000F の ADJUST_F に対応
// =========================================
const unsigned long T2_MIN    =    1000UL;   // WAIT_AFTER の下限(ms)
const unsigned long T2_MAX    =  600000UL;   // WAIT_AFTER の上限(ms) ≈ 10分
const int           NC_MARGIN =       20;    // 引き込み防止マージン（Nc最大値から引く）

// =========================================
//   タイムアウト設定
// =========================================
const unsigned long TIMEOUT_MS = 10000UL;    // 完了後に自動停止するまでの時間(ms)

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
const int PIN_LED2   = 4;  // 赤（完了）

// =========================================
//   状態管理
// =========================================
enum State { WAITING, RUNNING, DONE, STOPPED };
State state = WAITING;

// =========================================
//   自動計算関数
//
//   計算式:
//     F = FC×Nc + F_BEFORE_MS×WAIT_BEFORE + F_AFTER_MS×WAIT_AFTER + BASE_CONST
//
//   Nc       : BASE_CONST（名目値）のみで計算 → ADJUST_F の影響を受けない
//   WAIT_AFTER : BASE_CONST + ADJUST_F で計算 → 誤差を吸収
// =========================================
void calcParams() {
  // Nc の計算（名目値のみ使用・ADJUST_F は使わない）
  float fixed_nominal = F_BEFORE_MS * WAIT_BEFORE + BASE_CONST;
  float nc_max_f = (TARGET_FRAME - fixed_nominal - F_AFTER_MS * T2_MIN) / FC;
  long nc = (nc_max_f > 0) ? (long)nc_max_f - NC_MARGIN : 0L;
  NUM_CONTINUE = (nc > 0) ? (unsigned long)nc : 0UL;

  // WAIT_AFTER の計算（ADJUST_F を加味して誤差を吸収）
  float fixed_adjusted = fixed_nominal + ADJUST_F;
  float t2 = (TARGET_FRAME - FC * NUM_CONTINUE - fixed_adjusted) / F_AFTER_MS;

  // クランプ
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
}

void loop() {
  if (state == WAITING) {
    SwitchControlLibrary().sendReport();
    delay(100);

    if (digitalRead(PIN_BUTTON) == LOW) {
      delay(50);
      state = RUNNING;
    }
  }

  if (state == RUNNING) {
    digitalWrite(PIN_LED1, HIGH);
    runMacro();
    digitalWrite(PIN_LED1, LOW);
    state = DONE;
  }

  if (state == DONE) {
    // 赤LED点灯・TIMEOUT_MS 秒間 sendReport しながら待機
    digitalWrite(PIN_LED2, HIGH);
    unsigned long n   = TIMEOUT_MS / 100;
    unsigned long rem = TIMEOUT_MS % 100;
    for (unsigned long i = 0; i < n; i++) {
      SwitchControlLibrary().sendReport();
      delay(100);
    }
    if (rem > 0) delay(rem);

    // タイムアウト → 赤LED消灯して完全停止
    digitalWrite(PIN_LED2, LOW);
    state = STOPPED;
  }

  if (state == STOPPED) {
    // 何もしない（リセットボタンまたは抜き差しで再起動）
    while (true) {}
  }
}

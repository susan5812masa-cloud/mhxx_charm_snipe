import cv2
import numpy as np
import pytesseract
import re
import csv
import os
from datetime import datetime
from difflib import get_close_matches

# ===== 設定 =====
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

TEMPLATE_CIRCLE = r'F:\Workspace\Python\mhxx-capture\test\template_circle.png'
TEMPLATE_DASH   = r'F:\Workspace\Python\mhxx-capture\test\template_dash.png'
OUTPUT_CSV      = r'F:\Workspace\Python\mhxx-capture\talisman_log.csv'

KNOWN_SKILLS = [
    # スキル1候補
    "聴覚保護", "風圧", "寒冷適応", "炎熱適応", "狂撃耐性", "細菌学",
    "属性耐性", "属性攻撃", "特殊攻撃", "斬れ味", "剣術", "研磨術",
    "鈍器", "抜刀会心", "抜刀減気", "納刀", "納刀研磨", "装填速度",
    "反動", "通常弾強化", "貫通弾強化", "散弾強化", "重撃弾強化",
    "速射", "射法", "装填数", "弾薬節約", "痛撃", "連撃",
    "特殊会心", "属性会心", "溜め短縮", "スタミナ", "体術", "気力回復",
    "走行継続", "回避性能", "回避距離", "泡沫", "ガード性能", "ガード強化",
    "KO", "減気攻撃", "重撃", "本気", "闘魂", "無傷", "チャンス",
    "底力", "逆上", "窮地", "根性", "跳躍", "無心", "我慢", "SP延長",
    "加護", "英雄の盾", "回復量", "食事", "節食", "護石王",
    # スキル2のみ
    "攻撃", "防御", "火属性攻撃", "水属性攻撃", "雷属性攻撃",
    "氷属性攻撃", "龍属性攻撃", "研ぎ師", "匠", "刃鱗", "達人",
    "会心強化", "裏会心", "笛", "砲術", "爆弾強化", "龍気", "乗り",
    "広域", "茸食", "運気", "剥ぎ取り", "捕獲",
    # 二つ名
    "真・紅兜", "真・大雪主", "真・矛砕", "真・岩穿", "真・紫毒姫",
    "真・宝纏", "真・白疾風", "真・隻眼", "真・黒炎王", "真・金雷公",
    "真・荒鉤爪", "真・燼滅刃", "真・朧隠", "真・鎧裂", "真・天眼",
    "真・青電主", "真・銀嶺", "真・鏖魔",
]

# KNOWN_SKILLSの直後に追加
OCR_CORRECTION = {
    "理会": "裏会心",
    "裏会": "裏会心",
    "裏会c": "裏会心",
    "特殊会": "特殊会心",
    "超会": "超会心",
    "弱点特": "弱点特効",
    "走行継": "走行継続",
    "装填速": "装填速度",
    "刃鱗": "刃鱗",
    "灸": "刃鱗",    # ← 追加
    "刃麟": "刃鱗",  # ← 追加
}

# ===== OCR関連 =====
def fuzzy_match(name):
    # まず補正辞書を優先チェック
    for key, val in OCR_CORRECTION.items():
        if key in name:
            return val
    matches = get_close_matches(name, KNOWN_SKILLS, n=1, cutoff=0.4)
    return matches[0] if matches else None

def extract_value(text):
    m = re.search(r'[+\-]\s*\d+', text)
    return m.group().replace(' ', '') if m else None

def extract_name(text):
    name = re.sub(r'[+\-]\s*\d+', '', text)
    name = re.sub(r'\s+', '', name).strip()
    # OCR補正辞書は1文字でも先にチェック
    for key, val in OCR_CORRECTION.items():
        if key in name:
            return val
    return fuzzy_match(name) if len(name) >= 2 else None

def read_skill(img):
    img2 = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)

    text1 = pytesseract.image_to_string(img, lang='jpn').strip()
    name1 = extract_name(text1)
    val1  = extract_value(text1)

    text2 = pytesseract.image_to_string(inverted, lang='jpn', config='--psm 7').strip()
    name2 = extract_name(text2)
    val2  = extract_value(text2)

    print(f"    [DEBUG] text1='{text1}' → name='{name1}' val='{val1}'")  # ← 追加
    print(f"    [DEBUG] text2='{text2}' → name='{name2}' val='{val2}'")  # ← 追加

    return name1 or name2, val1 or val2

# ===== スロット読み取り =====
def count_slots(slot_img, circle_tmpl, dash_tmpl, threshold=0.7):
    result = cv2.matchTemplate(slot_img, circle_tmpl, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    xs = locations[1]
    count = 0
    prev_x = -100
    for x in sorted(xs):
        if x - prev_x > 20:
            count += 1
            prev_x = x
    return count

# ===== メイン処理 =====
def read_talisman(image_path):
    print(f"\n[読み取り開始] {image_path}")

    # 画像読み込み
    img = cv2.imread(image_path)
    if img is None:
        print(f"エラー: 画像を読み込めませんでした → {image_path}")
        return None

    print(f"  画像サイズ: {img.shape[1]}x{img.shape[0]}")

    # 各領域の切り出し
    skill1_region = img[245:290, 950:1300]
    skill2_region = img[285:330, 950:1300]
    slot_region   = img[330:375, 700:1000]

    # スキル読み取り
    skill1_name, skill1_val = read_skill(skill1_region)
    skill2_name, skill2_val = read_skill(skill2_region)

    # スロット読み取り
    circle_tmpl = cv2.imread(TEMPLATE_CIRCLE)
    dash_tmpl   = cv2.imread(TEMPLATE_DASH)

    if circle_tmpl is None or dash_tmpl is None:
        print("警告: テンプレート画像が見つかりません。スロット数は0とします。")
        slots = 0
    else:
        slots = count_slots(slot_region, circle_tmpl, dash_tmpl)

    # 結果まとめ
    result = {
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image":       os.path.basename(image_path),
        "skill1_name": skill1_name or "不明",
        "skill1_val":  skill1_val  or "?",
        "skill2_name": skill2_name or "不明",
        "skill2_val":  skill2_val  or "?",
        "slots":       slots,
    }

    return result

def print_result(result):
    print("\n===== 護石鑑定結果 =====")
    print(f"  スキル1 : {result['skill1_name']} {result['skill1_val']}")
    print(f"  スキル2 : {result['skill2_name']} {result['skill2_val']}")
    print(f"  スロット : {result['slots']}個")
    print("========================\n")

def save_to_csv(result):
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()  # 初回のみヘッダーを書く
        writer.writerow(result)
    print(f"[CSV保存] {OUTPUT_CSV}")

# ===== エントリーポイント =====
if __name__ == "__main__":
    from find_frame import find_frame

    IMAGE_PATH = r'F:\Workspace\Python\mhxx-capture\test\sample.png'

# ===== 欲しい護石の設定 =====
    # ▼ WANT_SKILL1は以下から選んでコピペ（スキル1に設定できるもの）
    # '聴覚保護' '風圧'      '寒冷適応'  '炎熱適応'  '狂撃耐性'  '細菌学'
    # '属性耐性' '属性攻撃'  '特殊攻撃'  '斬れ味'    '剣術'      '研磨術'
    # '鈍器'     '抜刀会心'  '抜刀減気'  '納刀'      '納刀研磨'  '装填速度'
    # '反動'     '通常弾強化''貫通弾強化''散弾強化'  '重撃弾強化''速射'
    # '射法'     '装填数'    '弾薬節約'  '痛撃'      '連撃'      '特殊会心'
    # '属性会心' '溜め短縮'  'スタミナ'  '体術'      '気力回復'  '走行継続'
    # '回避性能' '回避距離'  '泡沫'      'ガード性能' 'ガード強化' 'KO'
    # '減気攻撃' '重撃'      '本気'      '闘魂'      '無傷'      'チャンス'
    # '底力'     '逆上'      '窮地'      '根性'      '跳躍'      '無心'
    # '我慢'     'SP延長'    '加護'      '英雄の盾'  '回復量'    '食事'
    # '節食'     '護石王'
    #
    # ▼ WANT_SKILL2は上記に加えて以下も設定できる（スキル2のみ）
    # '攻撃'     '防御'      '火属性攻撃''水属性攻撃''雷属性攻撃''氷属性攻撃'
    # '龍属性攻撃''研ぎ師'   '匠'        '刃鱗'      '達人'      '会心強化'
    # '裏会心'   '笛'        '砲術'      '爆弾強化'  '龍気'      '乗り'
    # '広域'     '茸食'      '運気'      '剥ぎ取り'  '捕獲'
    # --- 二つ名スキル（スキル2のみ）---
    # '真・紅兜' '真・大雪主''真・矛砕'  '真・岩穿'  '真・紫毒姫''真・宝纏'
    # '真・白疾風''真・隻眼' '真・黒炎王''真・金雷公''真・荒鉤爪''真・燼滅刃'
    # '真・朧隠' '真・鎧裂'  '真・天眼'  '真・青電主''真・銀嶺'  '真・鏖魔'
    # ※ スキル2なしの場合は WANT_SKILL2 = None, WANT_VAL2 = 0
    # ---------------------------------------------------------

    WANT_SKILL1 = '痛撃'
    WANT_VAL1   = 6
    WANT_SKILL2 = '会心強化'
    WANT_VAL2   = 5
    WANT_SLOTS  = 3

    # ターゲットフレームを自動計算（起動時に1回だけ実行）
    print("[ターゲット検索中...]")
    target_frames = find_frame(WANT_SKILL1, f'+{WANT_VAL1}',
                               WANT_SKILL2, f'+{WANT_VAL2}',
                               WANT_SLOTS, max_frame=10**7)
    if not target_frames:
        print("[ERROR] ターゲット護石が見つかりません")
        exit()

    TARGET_FRAME = min(target_frames)
    print(f"[ターゲット決定] {TARGET_FRAME:,}F\n")

    # OCR → フレーム検索 → 差分計算
    result = read_talisman(IMAGE_PATH)
    if result:
        print_result(result)
        save_to_csv(result)

        frames = find_frame(
            result['skill1_name'], result['skill1_val'],
            result['skill2_name'], result['skill2_val'],
            result['slots'],
            max_frame=10**7
        )

        if frames:
            closest = min(frames, key=lambda x: abs(x - TARGET_FRAME))
            diff = closest - TARGET_FRAME
            diff_ms = int(diff / 30 * 1000)
            print(f"\n[最も近いフレーム]")
            print(f"  ターゲット : {TARGET_FRAME:,}F")
            print(f"  最近傍    : {closest:,}F")
            print(f"  差分      : {diff:+,}F  ({diff_ms:+,}ms)")
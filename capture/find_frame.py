# find_frame.py
# mhxx-rngを使って護石のフレーム数を検索するモジュール

import os as _os
import json as _json
MHXX_RNG_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'mhxx-rng-main', 'mhxx-rng.ipynb')

# ===== mhxx-rng の初期グローバル変数 =====
s = [0x0194FD72, 0x79E6C985, 0x08DD9701, 0x41CFCE91]
x, y, z, w, t, f = 0, 0, 0, 0, 0, 0
r0, r1, r2, r3, r4, r5, r6 = 0, 0, 0, 0, 0, 0, 0
num_of_charms = 40
showallrank = True
showrare = True

# ===== mhxx-rng の定義部分のみ読み込む（.ipynbから直接取得）=====
with open(MHXX_RNG_PATH, 'r', encoding='utf-8') as _f:
    _nb = _json.load(_f)

# コードセルのソースを結合して行リストを作成
_lines = []
for _cell in _nb['cells']:
    if _cell['cell_type'] == 'code':
        _src = _cell['source']
        if isinstance(_src, str):
            _src = _src.splitlines(keepends=True)
        if _src and not _src[-1].endswith('\n'):
            _src = list(_src)
            _src[-1] += '\n'
        _lines.extend(_src)

# セクション境界を検出
_first_start  = next(i for i, l in enumerate(_lines) if '# @title 1st' in l)
_second_start = next(i for i, l in enumerate(_lines) if 'import numpy as np' in l)
_third_start  = next(i for i, l in enumerate(_lines) if '# @title 3rd' in l)

# 3rd（スキル名テーブル）→ 1st（関数定義）の順に実行。2nd（numba高速版）はスキップ
exec(''.join(_lines[_third_start:]), globals())          # set_ja() 等を定義
set_ja()                                                  # skill[], origin[] 等を設定
exec(''.join(_lines[_first_start:_second_start]), globals())  # 関数群を定義
init()
set_blue()  # 天の護石 = 風化したお守り（RARE8/9/10 → kind=0）

# ===== スキル名 マッピング =====
SKILL_NAME_MAP = {
    # ===== スキル1・スキル2 共通 =====
    '聴覚保護': '聴覚', '風圧':     '風圧', '寒冷適応': '寒冷', '炎熱適応': '炎熱',
    '狂撃耐性': '狂撃', '細菌学':   '細菌', '属性耐性': '属耐', '属性攻撃': '属攻',
    '特殊攻撃': '特攻', '斬れ味':   '斬味', '剣術':     '剣術', '研磨術':   '研磨',
    '鈍器':     '鈍器', '抜刀会心': '抜会', '抜刀減気': '抜減', '納刀':     '納刀',
    '納刀研磨': '納研', '装填速度': '装速', '反動':     '反動', '通常弾強化':'通強',
    '貫通弾強化':'貫強', '散弾強化': '散強', '重撃弾強化':'重強', '速射':    '速射',
    '射法':     '射法', '装填数':   '装数', '弾薬節約': '弾節', '痛撃':     '痛撃',
    '連撃':     '連撃', '特殊会心': '特会', '属性会心': '属会', '溜め短縮': '溜短',
    'スタミナ': 'スタ', '体術':     '体術', '気力回復': '気力', '走行継続': '走行',
    '回避性能': '回性', '回避距離': '回距', '泡沫':     '泡沫', 'ガード性能':'ガ性',
    'ガード強化':'ガ強', 'KO':       'ＫＯ', '減気攻撃': '減攻', '重撃':     '重撃',
    '本気':     '本気', '闘魂':     '闘魂', '無傷':     '無傷', 'チャンス':  'チャ',
    '底力':     '底力', '逆上':     '逆上', '窮地':     '窮地', '根性':     '根性',
    '跳躍':     '跳躍', '無心':     '無心', '我慢':     '我慢', 'SP延長':    'ＳＰ',
    '加護':     '加護', '英雄の盾': '英雄', '回復量':   '回量', '食事':     '食事',
    '節食':     '節食', '護石王':   '護石',
    # ===== スキル2のみ =====
    '攻撃':     '攻撃', '防御':     '防御', '火属性攻撃':'火攻', '水属性攻撃':'水攻',
    '雷属性攻撃':'雷攻', '氷属性攻撃':'氷攻', '龍属性攻撃':'龍攻', '研ぎ師':  '研師',
    '匠':       '匠　', '刃鱗':     '刃鱗', '達人':     '達人', '会心強化': '会心',
    '裏会心':   '裏会', '笛':       '笛　', '砲術':     '砲術', '爆弾強化': '爆弾',
    '龍気':     '龍気', '乗り':     '乗り', '広域':     '広域', '茸食':     '茸食',
    '運気':     '運気', '剥ぎ取り': '剥取', '捕獲':     '捕獲',
    # ===== 二つ名スキル（スキル2のみ）=====
    '真・紅兜':   '真紅', '真・大雪主': '真大', '真・矛砕':   '真矛',
    '真・岩穿':   '真岩', '真・紫毒姫': '真紫', '真・宝纏':   '真宝',
    '真・白疾風': '真白', '真・隻眼':   '真隻', '真・黒炎王': '真黒',
    '真・金雷公': '真金', '真・荒鉤爪': '真荒', '真・燼滅刃': '真燼',
    '真・朧隠':   '真朧', '真・鎧裂':   '真鎧', '真・天眼':   '真天',
    '真・青電主': '真青', '真・銀嶺':   '真銀', '真・鏖魔':   '真鏖',
    # ===== OCR誤読対策（略称でも受け付ける）=====
    '聴覚': '聴覚', '寒冷': '寒冷', '炎熱': '炎熱', '狂撃': '狂撃',
    '細菌': '細菌', '属耐': '属耐', '属攻': '属攻', '特攻': '特攻',
    '斬味': '斬味', '研磨': '研磨', '抜会': '抜会', '抜減': '抜減',
    '納研': '納研', '装速': '装速', '通強': '通強', '貫強': '貫強',
    '散強': '散強', '重強': '重強', '弾節': '弾節', '特会': '特会',
    '属会': '属会', '溜短': '溜短', 'スタ': 'スタ', '気力': '気力',
    '走行': '走行', '回性': '回性', '回距': '回距', 'ガ性': 'ガ性',
    'ガ強': 'ガ強', 'ＫＯ': 'ＫＯ', '減攻': '減攻', 'チャ': 'チャ',
    '逆上': '逆上', '根性': '根性', 'ＳＰ': 'ＳＰ', '英雄': '英雄',
    '回量': '回量', '護石': '護石', '火攻': '火攻', '水攻': '水攻',
    '雷攻': '雷攻', '氷攻': '氷攻', '龍攻': '龍攻', '研師': '研師',
    '会心': '会心', '裏会': '真紅', '剥取': '剥取',
    '超会心': '特会',  # OCR誤認識対策
}

def find_frame(skill1_name, skill1_val, skill2_name, skill2_val, slots,
               start_frame=0, max_frame=10**7):
    rng_skill1 = SKILL_NAME_MAP.get(skill1_name)
    if rng_skill1 is None:
        print(f"[ERROR] スキル1 '{skill1_name}' がSKILL_NAME_MAPにありません")
        return []

    # val1 の検証（'?' や None はエラー扱い）
    _val1_str = str(skill1_val).replace('+', '').strip()
    if not _val1_str.lstrip('-').isdigit():
        print(f"[ERROR] スキル1の値が無効です: '{skill1_val}' （OCR失敗の可能性）")
        return []
    val1 = int(_val1_str)
    val2 = int(str(skill2_val).replace('+', '')) if skill2_val not in (None, '?') else 0

    # スキル2が不明かどうか判定
    no_skill2 = skill2_name in (None, '不明', '') or SKILL_NAME_MAP.get(skill2_name) is None
    rng_skill2 = SKILL_NAME_MAP.get(skill2_name) if not no_skill2 else None

    if no_skill2:
        print(f"\n[検索開始] {rng_skill1}{val1:+d} / スキル2なし スロット{slots}")
    else:
        print(f"\n[検索開始] {rng_skill1}{val1:+d} / {rng_skill2}{val2:+d} スロット{slots}")
    print(f"  検索範囲: {start_frame:,}〜{max_frame:,}F")

    set_blue()
    init()
    jump(start_frame)

    found = []
    search_count = max_frame - start_frame

    if no_skill2:
        # スキル2なし → search_greater_skill1 相当
        try:
            p = parameter(rng_skill1, val1, '達人', 1, slots, 'マカ')  # skill2はダミー
        except (ValueError, IndexError) as e:
            print(f"[ERROR] parameter() 失敗（スキル1が護石skill1として無効な可能性）: {e}")
            print(f"  スキル1='{skill1_name}'({rng_skill1}) val={val1} スロット={slots}")
            return []
        _id1, _sp1, _id2, _sp2, _slot, _origin, _len1, _len2 = p
        for i in range(search_count):
            roll()
            if r0 % _len1 == _id1:
                c = getcharm(_origin)
                if c[1] == _sp1 and c[4] == _slot:
                    frame = f - 7
                    # print(f"  ヒット: {frame}F")
                    found.append(frame)
    else:
        # スキル2あり → 通常のsearch
        try:
            p = parameter(rng_skill1, val1, rng_skill2, val2, slots, 'マカ')
        except (ValueError, IndexError) as e:
            print(f"[ERROR] parameter() 失敗（スキルの組み合わせが無効な可能性）: {e}")
            print(f"  スキル1='{skill1_name}'({rng_skill1}{val1:+d}) スキル2='{skill2_name}'({rng_skill2}{val2:+d}) スロット={slots}")
            return []
        _id1, _sp1, _id2, _sp2, _slot, _origin, _len1, _len2 = p
        for i in range(search_count):
            roll()
            if r0 % _len1 == _id1 and r2 % 100 >= th and r3 % _len2 == _id2:
                c = getcharm(_origin)
                if c[1] == _sp1 and c[3] == _sp2 and c[4] == _slot:
                    frame = f - 7
                    # print(f"  ヒット: {frame}F")
                    found.append(frame)

    if not found:
        print("  結果なし")
    else:
        print(f"  合計 {len(found)}件 ヒット")

    return found


if __name__ == '__main__':
    # テスト: sample.pngの護石（本気+6 / 裏会心+2 / スロット0）
    results = find_frame('本気', '+6', '裏会心', '+2', 0, max_frame=10**7)
    print(results[:5])
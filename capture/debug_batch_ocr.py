"""
debug_batch_ocr.py - screenshots/ 内の全画像に対してOCRを一括実行し結果をCSV出力する

使い方:
  python capture/debug_batch_ocr.py

出力:
  capture/debug_ocr_result.csv  （画像ファイル名・スキル名・値・スロット・備考）
  コンソールには処理進捗と警告サマリーを表示。
"""

import sys
import os
import csv
import io

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _BASE_DIR)

from read_talisman import read_talisman

SCREENSHOT_DIR = os.path.join(_BASE_DIR, 'screenshots')
OUTPUT_CSV     = os.path.join(_BASE_DIR, 'debug_ocr_result.csv')

CSV_FIELDS = [
    'image',
    'skill1_name', 'skill1_val',
    'skill2_name', 'skill2_val',
    'slots',
    'note',
]

def main():
    png_files = sorted(
        f for f in os.listdir(SCREENSHOT_DIR) if f.lower().endswith('.png')
    )
    if not png_files:
        print(f"[ERROR] {SCREENSHOT_DIR} にPNG画像が見つかりません")
        sys.exit(1)

    print(f"対象画像数: {len(png_files)} 枚")
    print(f"出力先: {OUTPUT_CSV}\n")

    rows     = []
    warnings = []

    for fname in png_files:
        path = os.path.join(SCREENSHOT_DIR, fname)

        # DEBUGログを抑制
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            result = read_talisman(path)
        finally:
            sys.stdout = old_stdout

        if result is None:
            note = "読み取り失敗"
            rows.append({
                'image':       fname,
                'skill1_name': '',
                'skill1_val':  '',
                'skill2_name': '',
                'skill2_val':  '',
                'slots':       '',
                'note':        note,
            })
            warnings.append((fname, note))
            print(f"  [NG] {fname}  → {note}")
            continue

        s1n   = result['skill1_name']
        s1v   = result['skill1_val']
        s2n   = result['skill2_name']
        s2v   = result['skill2_val']
        slots = result['slots']

        issues = []
        if s1v == '?':
            issues.append("skill1_val=?")
        if s2v == '?':
            issues.append("skill2_val=?")
        if s1n == '不明':
            issues.append("skill1_name=不明")
        if s2n == '不明':
            issues.append("skill2_name=不明")

        note = " / ".join(issues) if issues else "OK"
        rows.append({
            'image':       fname,
            'skill1_name': s1n,
            'skill1_val':  s1v,
            'skill2_name': s2n,
            'skill2_val':  s2v,
            'slots':       slots,
            'note':        note,
        })

        if issues:
            warnings.append((fname, note))
            print(f"  [NG] {fname}  → {note}")
        else:
            print(f"  [OK] {fname}  {s1n} {s1v} / {s2n} {s2v} / {slots}個")

    # CSV書き出し
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n完了: {len(png_files)} 枚処理 → {OUTPUT_CSV}")

    if warnings:
        print(f"\n[警告あり: {len(warnings)} 件]")
        for fname, reason in warnings:
            print(f"  {fname}: {reason}")
    else:
        print("[OK] 全画像で値・スキル名の読み取り成功（'?' なし）")


if __name__ == "__main__":
    main()

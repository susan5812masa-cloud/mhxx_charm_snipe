import cv2
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(_BASE_DIR, 'screenshots')
output_dir = os.path.join(_BASE_DIR, 'test')
os.makedirs(output_dir, exist_ok=True)

files = sorted([f for f in os.listdir(input_dir) if f.endswith(".png")])
print(f"見つかったファイル数：{len(files)}")
print(files)

for filename in files:
    path = os.path.join(input_dir, filename)
    img = cv2.imread(path)

    if img is None:
        print(f"読み込み失敗：{path}")
        continue

    print(f"読み込み成功：{filename}　サイズ：{img.shape}")
    base = os.path.splitext(filename)[0]

    panel         = img[130:500, 700:1300]
    skill1_region = img[245:290, 950:1300]
    skill2_region = img[285:330, 950:1300]
    slot_region   = img[330:375, 700:1000]

    cv2.imwrite(os.path.join(output_dir, f"{base}_panel.png"),  panel)
    cv2.imwrite(os.path.join(output_dir, f"{base}_skill1.png"), skill1_region)
    cv2.imwrite(os.path.join(output_dir, f"{base}_skill2.png"), skill2_region)
    cv2.imwrite(os.path.join(output_dir, f"{base}_slot.png"),   slot_region)
    print(f"保存完了：{filename}")

print("全ファイル処理完了！")
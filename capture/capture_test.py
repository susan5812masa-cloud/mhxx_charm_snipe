import cv2
import os

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# スクショ保存フォルダ
save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(save_dir, exist_ok=True)
count = 0

if not cap.isOpened():
    print("デバイス0 は開けませんでした")
else:
    print("デバイス0 で接続成功！")
    print("スペースキー：スクリーンショット保存　q：終了")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("capture", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            filename = os.path.join(save_dir, f"screenshot_{count:03d}.png")
            cv2.imwrite(filename, frame)
            print(f"保存しました：{filename}")
            count += 1
        if cv2.getWindowProperty("capture", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
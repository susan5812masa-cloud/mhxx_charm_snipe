import pytesseract
import cv2
import re
from difflib import get_close_matches

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

KNOWN_SKILLS = [
    "本気", "裏会心", "特殊会心", "風圧", "スタミナ", "龍属性攻撃",
    "装填数", "走行継続", "斬れ味", "捕獲", "痛撃", "達人", "連撃",
    "攻撃", "防御", "耐震", "耐風圧", "挑戦者", "回避性能", "回避距離",
    "弱点特効", "超会心", "整備", "早食い", "採取"
]

def fuzzy_match(name):
    matches = get_close_matches(name, KNOWN_SKILLS, n=1, cutoff=0.4)
    return matches[0] if matches else None

def extract_value(text):
    m = re.search(r'[+\-]\s*\d+', text)
    return m.group().replace(' ', '') if m else None

def extract_name(text):
    name = re.sub(r'[+\-]\s*\d+', '', text)
    name = re.sub(r'\s+', '', name).strip()
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

    return name1 or name2, val1 or val2
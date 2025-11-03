"""
Object Counting System - Konfiguratsiya Fayli
Bu yerda tizimning barcha sozlamalari saqlanadi
"""

import os
from pathlib import Path

# Asosiy papkalar
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
INPUT_DIR = BASE_DIR / "input_videos"
OUTPUT_DIR = BASE_DIR / "output_videos"

# Papkalarni yaratish
MODELS_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# YOLO Model sozlamalari
YOLO_MODEL = "yolov8n.pt"  # n=nano (tez), s=small, m=medium, l=large, x=xlarge
CONFIDENCE_THRESHOLD = 0.5  # Ishonch darajasi (0.0 - 1.0)
IOU_THRESHOLD = 0.45       # Intersection Over Union threshold

# Sanash uchun obyekt klasslari (COCO dataset klasslari)
# 0: person, 2: car, 3: motorcycle, 5: bus, 7: truck
COUNT_CLASSES = {
    0: "Odam",           # person
    2: "Mashina",        # car
    3: "Mototsikl",      # motorcycle
    5: "Avtobus",        # bus
    7: "Yuk mashinasi",  # truck
    1: "Velosiped",      # bicycle
}

# Tracking sozlamalari
MAX_DISAPPEARED = 50        # Obyekt yo'qolgandan keyin necha frame kutish
MAX_DISTANCE = 50           # Tracking uchun maksimal masofa (pixel)

# Video sozlamalari
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# Chizish sozlamalari
BOX_COLOR = (0, 255, 0)        # Yashil (BGR formatda)
TEXT_COLOR = (255, 255, 255)   # Oq
LINE_COLOR = (0, 0, 255)       # Qizil (sanash chizig'i uchun)
LINE_THICKNESS = 2
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6

# Sanash chizig'i pozitsiyasi (ekranning qayerida)
# Y koordinatasi (0.0 - 1.0, ekranning yuqorisidan necha foizda)
COUNTING_LINE_POSITION = 0.5  # Ekranning o'rtasida

# Real-time processing sozlamalari
SKIP_FRAMES = 2  # Har nechinchi frameni qayta ishlash (tezlik uchun)
DISPLAY_OUTPUT = True  # Ekranda ko'rsatish

# Statistika sozlamalari
SAVE_STATISTICS = True  # Statistikani CSV faylga saqlash
STATS_FILENAME = "counting_stats.csv"

# Debug rejimi
DEBUG_MODE = False  # True bo'lsa, ko'proq ma'lumot chiqaradi

# Kamera sozlamalari (real-time uchun)
CAMERA_ID = 0  # Default kamera
CAMERA_RESOLUTION = (1280, 720)

# Performance sozlamalari
USE_GPU = True  # GPU mavjud bo'lsa ishlatish

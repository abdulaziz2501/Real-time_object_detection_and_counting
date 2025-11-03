# ⚡ Tezkor Boshlash - Object Counting System

## 🚀 3 Daqiqada Ishga Tushirish

### Windows

```bash
# 1. O'rnatish (bir marta)
install.bat

# 2. Ishga tushirish
run.bat
```

### Linux/Mac

```bash
# 1. O'rnatish (bir marta)
bash install.sh

# 2. Ishga tushirish
bash run.sh
```

## 💡 Oddiy Misollar

### 1. Kamera bilan ishlash
```bash
python app.py --camera
```

### 2. Video qayta ishlash
```bash
python app.py --video my_video.mp4 --save
```

### 3. Barcha parametrlar
```bash
python app.py --video test.mp4 --model yolov8s.pt --confidence 0.6 --save
```

## 📁 Test Video Qo'shish

```
object-counting-system/
└── input_videos/
    └── test.mp4      ← Bu yerga video qo'ying
```

## 🎯 Natijalar

```
object-counting-system/
└── output_videos/
    ├── test_counted.mp4         ← Qayta ishlangan video
    └── counting_stats.csv       ← Statistika
```

## ⚙️ Sozlamalar

`config.py` faylini tahrirlang:

```python
# Model tanlash (tez/aniq)
YOLO_MODEL = "yolov8n.pt"  # n=tez, m=o'rtacha, l=aniq

# Sanash chizig'i pozitsiyasi
COUNTING_LINE_POSITION = 0.5  # 0.0=yuqorida, 1.0=pastda

# Performance
SKIP_FRAMES = 2  # Katta son = tezroq, aniqlik kamroq
```

## 🔧 Muammo Yechimi

### Model yuklanmayapti?
```bash
# Internet kerak - model avtomatik yuklanadi
# Yoki: models/ papkaga yolov8n.pt ni qo'ying
```

### Video ochilmayapti?
```bash
# ffmpeg o'rnatish
# Ubuntu: sudo apt-get install ffmpeg
# Windows: ffmpeg.org dan yuklab oling
```

### Slow performance?
```python
# config.py da:
SKIP_FRAMES = 3
YOLO_MODEL = "yolov8n.pt"
```

## 📞 Yordam

- README.md - To'liq yo'riqnoma
- example.py - Ko'proq misollar
- config.py - Barcha sozlamalar

## 🎓 Keyingi Qadamlar

1. ✅ Kameradan test qiling
2. ✅ O'z videongizni qayta ishlang
3. ✅ Sozlamalarni o'zgartiring
4. ✅ CSV statistikani tahlil qiling

---

**Muvaffaqiyatlar! 🚀**

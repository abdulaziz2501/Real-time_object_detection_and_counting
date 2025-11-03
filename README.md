# 🎯 Object Counting System - Obyektlarni Sanash Tizimi

YOLOv8 va OpenCV asosida ishlaydigan aqlli kamera tizimi. Odamlar, mashinalar va boshqa obyektlarni real-time aniqlaydi va sanaydi.

## 📋 Imkoniyatlar

- ✅ Real-time obyekt aniqlash (YOLOv8)
- ✅ Obyektlarni tracking va ID berish
- ✅ Virtual chiziqdan o'tishni sanash
- ✅ Video va kamera bilan ishlash
- ✅ Ko'p xil obyekt turlarini sanash (odam, mashina, velosiped, va boshqalar)
- ✅ Natija videoni saqlash
- ✅ Statistikani CSV ga eksport qilish
- ✅ GPU/CPU support
- ✅ O'zbek tilida interface

## 🚀 Tezkor Boshlash

### 1. O'rnatish

```bash
# Virtual environment yaratish (tavsiya etiladi)
python -m venv venv

# Virtual environment'ni faollashtirish
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt
```

### 2. Birinchi Ishga Tushirish

```bash
# Test videoni qayta ishlash (model avtomatik yuklab olinadi)
python app.py --video input_videos/test.mp4 --save

# Kameradan foydalanish
python app.py --camera

# Faqat saqlash, ekranda ko'rsatmaslik
python app.py --video test.mp4 --save --no-display
```

## 📁 Loyiha Strukturasi

```
object-counting-system/
├── app.py                    # Asosiy dastur
├── counter.py                # Counting logikasi
├── utils.py                  # Yordamchi funksiyalar
├── config.py                 # Sozlamalar
├── requirements.txt          # Python kutubxonalari
├── .env.example             # Environment o'zgaruvchilar
├── README.md                # Bu fayl
├── models/                  # YOLO modellari (avtomatik yuklanadi)
│   └── yolov8n.pt
├── input_videos/            # Kirish videolar
│   └── test.mp4
└── output_videos/           # Natija videolar va statistika
    ├── test_counted.mp4
    └── counting_stats.csv
```

## 💻 Ishlatish

### Video bilan ishlash

```bash
# Oddiy rejim
python app.py --video my_video.mp4

# Natijani saqlash
python app.py --video my_video.mp4 --save

# Custom output nomi
python app.py --video my_video.mp4 --output result.mp4

# Faqat saqlash (ekranda ko'rsatmaslik)
python app.py --video my_video.mp4 --save --no-display
```

### Kamera bilan ishlash

```bash
# Default kamera (0)
python app.py --camera

# Boshqa kamera
python app.py --camera --camera-id 1
```

### Qo'shimcha parametrlar

```bash
# Custom model ishlatish
python app.py --video test.mp4 --model yolov8m.pt

# Confidence threshold o'zgartirish
python app.py --video test.mp4 --confidence 0.7

# Barcha parametrlar bilan
python app.py --video test.mp4 --model yolov8s.pt --confidence 0.6 --save --output custom_output.mp4
```

## ⚙️ Sozlamalar

`config.py` faylida barcha sozlamalar mavjud:

### YOLO Model

```python
YOLO_MODEL = "yolov8n.pt"  # n=nano (tez), s=small, m=medium, l=large, x=xlarge
CONFIDENCE_THRESHOLD = 0.5  # Ishonch darajasi
```

### Sanash sozlamalari

```python
COUNT_CLASSES = {
    0: "Odam",           # person
    2: "Mashina",        # car
    3: "Mototsikl",      # motorcycle
    5: "Avtobus",        # bus
    7: "Yuk mashinasi",  # truck
}

COUNTING_LINE_POSITION = 0.5  # Ekranning qayerida (0.0-1.0)
```

### Performance

```python
USE_GPU = True          # GPU ishlatish
SKIP_FRAMES = 2         # Har nechinchi frameni qayta ishlash
```

## 📊 Chiqish Formatlari

### 1. Video
- Qayta ishlangan video `output_videos/` papkasida
- Har bir obyekt bilan ID va box
- Sanash chizig'i ko'rsatilgan
- Real-time statistika

### 2. CSV Statistika
```csv
Timestamp,Odam,Mashina,Mototsikl,Avtobus,Yuk mashinasi
2024-01-15 14:30:00,45,23,5,2,8
```

## 🎯 YOLO Modellari

| Model | Razmer | Tezlik | Aniqlik |
|-------|--------|--------|---------|
| YOLOv8n | ~6MB | Juda tez | Yaxshi |
| YOLOv8s | ~22MB | Tez | Yaxshi+ |
| YOLOv8m | ~52MB | O'rtacha | Zo'r |
| YOLOv8l | ~87MB | Sekin | Juda zo'r |
| YOLOv8x | ~136MB | Juda sekin | Eng zo'r |

**Tavsiya:** 
- Tez ishlash kerak bo'lsa: `yolov8n.pt`
- Balans (tezlik + aniqlik): `yolov8s.pt` yoki `yolov8m.pt`
- Eng yuqori aniqlik: `yolov8l.pt` yoki `yolov8x.pt`

## 🔧 Muammolarni Hal Qilish

### 1. CUDA/GPU muammolari

```bash
# PyTorch CUDA versiyasini o'rnatish
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 2. OpenCV video codec muammolari

```bash
# ffmpeg o'rnatish
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows: ffmpeg.org dan yuklab olish
# Mac:
brew install ffmpeg
```

### 3. Kamera ochilmasa

```python
# config.py da kamera ID ni o'zgartiring
CAMERA_ID = 1  # yoki 2, 3...
```

### 4. Slow performance

```python
# config.py da:
SKIP_FRAMES = 3  # Ko'proq frameni skip qilish
YOLO_MODEL = "yolov8n.pt"  # Kichikroq model
USE_GPU = True  # GPU yoqish
```

## 📈 Qo'llanish Sohalari

1. **Savdo markazlari**
   - Tashrif buyuruvchilarni sanash
   - Navbatlarni monitoring qilish

2. **Yo'l nazorati**
   - Transport oqimini o'lchash
   - Tiqilinchlarni aniqlash

3. **Xavfsizlik tizimlari**
   - Kirish-chiqishni kuzatish
   - Anomaliyalarni aniqlash

4. **Tadbirlar va konferensiyalar**
   - Ishtirokchilarni sanash
   - Zal to'liqligini monitoring

5. **Parkinglar**
   - Bo'sh joylarni hisoblash
   - Kirish-chiqish statistikasi

## 🎓 Qanday Ishlaydi?

### 1. Detection (Aniqlash)
```
Video → YOLOv8 → Obyektlar koordinatalari
```

### 2. Tracking (Kuzatish)
```
Koordinatalar → Centroid Tracking → Har bir obyektga ID
```

### 3. Counting (Sanash)
```
Obyekt pozitsiyasi → Chiziqdan o'tdimi? → Statistikani yangilash
```

### 4. Visualization (Ko'rsatish)
```
Box + ID + Statistika → Video output
```

## 🔄 Kelajakda Qo'shilishi Mumkin

- [ ] Multi-camera support
- [ ] DeepSORT tracking
- [ ] Telegram bot integratsiyasi
- [ ] Web dashboard
- [ ] Cloud saqlash (AWS/GCP)
- [ ] Mobile ilova
- [ ] Custom training
- [ ] Heatmap visualization

## 🤝 Yordam va Support

Muammolar yoki savollar bo'lsa:

1. Config fayllarni tekshiring
2. Python versiyasini tekshiring (3.8+)
3. Dependencies to'g'ri o'rnatilganini tasdiqlang
4. Log fayllarni ko'ring

## 📝 Litsenziya

MIT License - erkin foydalanish mumkin.

## 👨‍💻 Muallif

Object Counting System - O'zbek dasturchilar uchun maxsus yaratilgan.

---

**Muvaffaqiyatlar! 🚀**

Savollar bo'lsa, so'rang - yordam beraman! 😊

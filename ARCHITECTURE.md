# 🏗️ Object Counting System - Arxitektura

## 📐 Tizim Dizayni

### Umumiy Oqim

```
Video Input → Frame Extraction → YOLO Detection → Tracking → Counting → Output
```

### Tafsilot

```
┌─────────────┐
│ Video/Camera│
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Frame Reader    │  ← OpenCV VideoCapture
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  YOLO Detection  │  ← Ultralytics YOLOv8
│  (GPU/CPU)       │     Obyektlarni aniqlash
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Object Tracker  │  ← Centroid Tracking
│  (ID Assignment) │     Har bir obyektga ID berish
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Line Crossing   │  ← Crossing Detection
│  Detection       │     Chiziqdan o'tishni tekshirish
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Counter Update  │  ← Statistics
│  & Statistics    │     Hisobni yangilash
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Visualization   │  ← Draw boxes, IDs, stats
│  & Output        │     Ko'rsatish va saqlash
└──────────────────┘
```

## 🧩 Modullar

### 1. config.py - Konfiguratsiya
```python
# Rol: Barcha sozlamalar
# Input: Yo'q
# Output: Config o'zgaruvchilari
# Dependencies: pathlib
```

**Asosiy sozlamalar:**
- YOLO model parametrlari
- Tracking sozlamalari
- Sanash chizig'i pozitsiyasi
- Visualization ranglari
- Performance sozlamalari

### 2. utils.py - Yordamchi Funksiyalar

#### ObjectTracker klassi
```python
# Rol: Obyektlarni kuzatish va ID berish
# Algoritm: Centroid Tracking
# Input: Detections [(x1,y1,x2,y2,class,conf)]
# Output: {object_id: (centroid, class, bbox)}
```

**Asosiy metodlar:**
- `register()` - Yangi obyekt qo'shish
- `deregister()` - Obyektni o'chirish
- `update()` - Frame yangilanishi

**Tracking logikasi:**
1. Har bir detection uchun centroid hisoblash
2. Mavjud obyektlar bilan masofalarni hisoblash
3. Hungarian algorithm (minimum distance matching)
4. Yangi obyektlarni ro'yxatga olish
5. Yo'qolgan obyektlarni kuzatish

#### Visualization funksiyalari
```python
draw_counting_line()    # Sanash chizig'ini chizish
draw_detection()        # Box va label chizish
draw_statistics()       # Statistika panelini chizish
```

#### Utility funksiyalar
```python
save_statistics_to_csv()  # CSV saqlash
get_video_writer()        # Video writer yaratish
format_time()             # Vaqt formatlash
```

### 3. counter.py - Asosiy Logika

#### ObjectCounter klassi
```python
# Rol: Detection, tracking, counting
# Input: Video/camera frames
# Output: Processed frames + statistics
```

**Asosiy metodlar:**

##### `detect_objects(frame)`
```python
# YOLO detection
Input: BGR frame
Process:
  1. Frame → YOLO model
  2. Filter by confidence
  3. Filter by class
Output: [(x1,y1,x2,y2,class_id,conf), ...]
```

##### `check_line_crossing(object_id, centroid)`
```python
# Chiziqdan o'tishni tekshirish
Input: Obyekt ID, joriy pozitsiya
Process:
  1. Oldingi pozitsiyani olish
  2. Chiziq o'rtasidami tekshirish
  3. Yo'nalishni aniqlash (yuqoridan/pastdan)
Output: True/False
```

##### `process_frame(frame)`
```python
# Bitta frame qayta ishlash
Input: Frame
Process:
  1. Chiziq chizish
  2. Detection
  3. Tracking
  4. Line crossing check
  5. Counter update
  6. Visualization
Output: Processed frame
```

##### `process_video(video_path)`
```python
# To'liq video qayta ishlash
Input: Video fayl yo'li
Process:
  1. Video ochish
  2. Frame-by-frame processing
  3. Progress tracking
  4. Video yozish (optional)
Output: Final statistics
```

### 4. app.py - Entry Point

```python
# Rol: CLI interface, argument parsing
# Flow:
#   1. Parse arguments
#   2. Download model (if needed)
#   3. Create ObjectCounter
#   4. Process video/camera
#   5. Save results
```

**CLI Commands:**
```bash
--video FILE        # Video input
--camera           # Camera input
--output FILE      # Output file name
--save             # Save video
--no-display       # Headless mode
--model MODEL      # YOLO model choice
--confidence FLOAT # Confidence threshold
```

## 🔄 Data Flow

### Frame Processing Pipeline

```python
Frame (H×W×3 BGR)
    ↓
YOLOv8 Model
    ↓
Detections [(x1,y1,x2,y2,cls,conf), ...]
    ↓
Tracker.update()
    ↓
Tracked Objects {id: (centroid, cls, bbox), ...}
    ↓
For each object:
    - Check line crossing
    - Update counter if crossed
    - Draw visualization
    ↓
Processed Frame
```

### Tracking State Management

```python
ObjectTracker State:
├── objects: {id: (cx, cy), ...}           # Joriy pozitsiyalar
├── disappeared: {id: frame_count, ...}    # Yo'qolgan framelar
└── next_object_id: int                    # Keyingi ID

Update Process:
1. Calculate centroids for new detections
2. Calculate distance matrix (old vs new)
3. Match using minimum distance
4. Register new objects
5. Update disappeared counters
6. Deregister old objects (max_disappeared exceeded)
```

### Counting Logic

```python
Counter State:
├── counted_ids: set()                     # Allaqachon sanangan obyektlar
├── stats: {class_name: count, ...}        # Statistika
└── previous_positions: {id: y, ...}       # Oldingi Y koordinatalari

Counting Process:
For each tracked object:
    if line_crossed(object_id, current_y):
        if object_id not in counted_ids:
            stats[class_name] += 1
            counted_ids.add(object_id)
```

## ⚡ Performance Optimizatsiya

### 1. Frame Skipping
```python
# Har nechinchi frameni qayta ishlash
if frame_count % (SKIP_FRAMES + 1) == 0:
    process_frame(frame)
```

**Trade-off:**
- ↑ SKIP_FRAMES → ↑ Tezlik, ↓ Aniqlik
- ↓ SKIP_FRAMES → ↓ Tezlik, ↑ Aniqlik

### 2. GPU Acceleration
```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)
```

**Tezlik taqqoslash:**
- CPU: ~5-10 FPS
- GPU (NVIDIA): ~30-60 FPS

### 3. Model Selection
```python
Model Size vs Speed:
├── yolov8n: ~6MB  → 60+ FPS (GPU)
├── yolov8s: ~22MB → 45+ FPS
├── yolov8m: ~52MB → 30+ FPS
├── yolov8l: ~87MB → 20+ FPS
└── yolov8x: ~136MB → 15+ FPS
```

### 4. Resolution Optimization
```python
# Katta videolarni kichikroq qilish
frame = cv2.resize(frame, (1280, 720))
```

## 🧪 Testing Strategy

### Unit Tests
```python
# test_tracker.py
- Test ObjectTracker.register()
- Test ObjectTracker.deregister()
- Test ObjectTracker.update()

# test_counter.py
- Test line crossing detection
- Test counting accuracy
- Test statistics update
```

### Integration Tests
```python
# test_end_to_end.py
- Test video processing pipeline
- Test camera input
- Test output file creation
```

## 🔒 Xavfsizlik

### Input Validation
```python
# Video fayl tekshirish
if not Path(video_path).exists():
    raise FileNotFoundError()

# Kamera tekshirish
if not cap.isOpened():
    raise ValueError("Camera not found")
```

### Error Handling
```python
try:
    # Processing
except Exception as e:
    logger.error(f"Error: {e}")
    # Cleanup
finally:
    cap.release()
    cv2.destroyAllWindows()
```

## 📊 Scalability

### Multi-Camera Support (Future)
```python
class MultiCameraCounter:
    def __init__(self, camera_ids):
        self.counters = [ObjectCounter() for _ in camera_ids]
    
    def process_all(self):
        # Parallel processing
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(counter.process_camera, cam_id)
                for counter, cam_id in zip(self.counters, camera_ids)
            ]
```

### Cloud Integration (Future)
```python
# AWS/GCP storage
def save_to_cloud(video_path, stats):
    # Upload to S3/GCS
    # Store statistics in database
    pass
```

## 🛠️ Maintenance

### Code Quality
- Type hints ishlatish
- Docstring yozish
- PEP 8 standartiga amal qilish
- Regular code review

### Monitoring
```python
# Logging
import logging
logger = logging.getLogger(__name__)

# Metrics
- Processing FPS
- Detection accuracy
- Memory usage
- GPU utilization
```

### Version Control
```bash
git tag v1.0.0
git tag v1.1.0  # Bug fixes
git tag v2.0.0  # Major features
```

---

**Arxitektura versiyasi:** 1.0  
**Oxirgi yangilanish:** 2024-11-03

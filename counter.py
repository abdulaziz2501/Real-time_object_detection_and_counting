"""
Object Counting System - Asosiy Sanash Logikasi
Bu modul obyektlarni aniqlash, kuzatish va sanashni amalga oshiradi
"""

import cv2
import numpy as np
from ultralytics import YOLO
import config
from utils import ObjectTracker, draw_counting_line, draw_detection, draw_statistics
import torch


class ObjectCounter:
    """
    Obyektlarni sanash uchun asosiy klass
    YOLO modelidan foydalanib, obyektlarni aniqlaydi va sanaydi
    """
    
    def __init__(self, model_path=None, count_classes=None):
        """
        Args:
            model_path: YOLO model fayl yo'li
            count_classes: Sanaladigan klaslar dict {class_id: name}
        """
        # YOLO modelini yuklash
        if model_path is None:
            model_path = str(config.MODELS_DIR / config.YOLO_MODEL)
        
        print("🔄 YOLO modeli yuklanmoqda...")
        
        # GPU/CPU tanlash
        device = 'cuda' if config.USE_GPU and torch.cuda.is_available() else 'cpu'
        print(f"📱 Qurilma: {device.upper()}")
        
        self.model = YOLO(model_path)
        self.model.to(device)
        
        print("✅ Model yuklandi!")
        
        # Sanash uchun klasslar
        self.count_classes = count_classes if count_classes else config.COUNT_CLASSES
        
        # Tracker
        self.tracker = ObjectTracker(
            max_disappeared=config.MAX_DISAPPEARED,
            max_distance=config.MAX_DISTANCE
        )
        
        # Sanash statistikasi
        self.counted_ids = set()  # O'tgan obyektlar ID
        self.stats = {name: 0 for name in self.count_classes.values()}
        
        # Chiziq pozitsiyasi
        self.line_y = None
        
        # Obyektlarning oldingi pozitsiyalari
        self.previous_positions = {}
    
    def detect_objects(self, frame):
        """
        Frameda obyektlarni aniqlash
        
        Args:
            frame: Video frame
        
        Returns:
            list: [(x1, y1, x2, y2, class_id, confidence), ...]
        """
        # YOLO orqali detection
        results = self.model(frame, conf=config.CONFIDENCE_THRESHOLD, 
                            iou=config.IOU_THRESHOLD, verbose=False)
        
        detections = []
        
        # Natijalarni qayta ishlash
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Koordinatalar va ma'lumotlar
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                # Faqat kerakli klasslarni olish
                if class_id in self.count_classes:
                    detections.append((x1, y1, x2, y2, class_id, confidence))
        
        return detections
    
    def check_line_crossing(self, object_id, current_centroid):
        """
        Obyekt chiziqdan o'tdimi yoki yo'qligini tekshirish
        
        Args:
            object_id: Obyekt ID
            current_centroid: Joriy centroid (cx, cy)
        
        Returns:
            bool: O'tgan bo'lsa True
        """
        if self.line_y is None:
            return False
        
        cy = current_centroid[1]
        
        # Agar obyekt avval ko'rilgan bo'lsa
        if object_id in self.previous_positions:
            prev_cy = self.previous_positions[object_id]
            
            # Yuqoridan pastga o'tdi
            if prev_cy < self.line_y <= cy:
                return True
            # Pastdan yuqoriga o'tdi
            elif prev_cy > self.line_y >= cy:
                return True
        
        # Pozitsiyani yangilash
        self.previous_positions[object_id] = cy
        
        return False
    
    def process_frame(self, frame):
        """
        Bitta frameni qayta ishlash
        
        Args:
            frame: Video frame
        
        Returns:
            frame: Qayta ishlangan frame
        """
        # Sanash chizig'ini chizish
        frame, self.line_y = draw_counting_line(frame, config.COUNTING_LINE_POSITION)
        
        # Obyektlarni aniqlash
        detections = self.detect_objects(frame)
        
        # Tracking va yangilash
        tracked_objects = self.tracker.update(detections)
        
        # Har bir kuzatilayotgan obyekt uchun
        for object_id, (centroid, class_id, bbox) in tracked_objects.items():
            class_name = self.count_classes[class_id]
            
            # Chiziqdan o'tishni tekshirish
            if self.check_line_crossing(object_id, centroid):
                # Agar bu obyekt avval sanalmagan bo'lsa
                if object_id not in self.counted_ids:
                    self.stats[class_name] += 1
                    self.counted_ids.add(object_id)
                    
                    if config.DEBUG_MODE:
                        print(f"✅ Sanalgan: {class_name} (ID: {object_id})")
            
            # Detection ma'lumotlarini topish
            for det in detections:
                if det[:4] == bbox:
                    confidence = det[5]
                    break
            else:
                confidence = 0.0
            
            # Chizish
            draw_detection(frame, bbox, object_id, class_name, confidence)
        
        # Statistikani ko'rsatish
        frame = draw_statistics(frame, self.stats)
        
        return frame
    
    def process_video(self, video_path, output_path=None, display=True):
        """
        Videoni to'liq qayta ishlash
        
        Args:
            video_path: Kirish video fayli
            output_path: Chiqish video fayli (optional)
            display: Ekranda ko'rsatish
        
        Returns:
            dict: Yakuniy statistika
        """
        print(f"\n🎥 Video ishlanmoqda: {video_path}")
        
        # Video ochish
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"❌ Video ochilmadi: {video_path}")
        
        # Video ma'lumotlari
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📊 FPS: {fps}, Razmer: {width}x{height}, Framelar: {total_frames}")
        
        # Video yozuvchi
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"💾 Natija saqlanadi: {output_path}")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                # Har bir frameni qayta ishlash (yoki skip qilish)
                if frame_count % (config.SKIP_FRAMES + 1) == 0:
                    processed_frame = self.process_frame(frame)
                    
                    # Video yozish
                    if out:
                        out.write(processed_frame)
                    
                    # Ekranda ko'rsatish
                    if display:
                        cv2.imshow('Object Counting System', processed_frame)
                        
                        # 'q' bosilsa to'xtatish
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            print("\n⏹️  Foydalanuvchi to'xtatdi")
                            break
                
                # Progress
                if frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"⏳ Jarayon: {progress:.1f}% ({frame_count}/{total_frames})")
        
        finally:
            # Resurslarni bo'shatish
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
        
        print("\n✅ Video qayta ishlash tugadi!")
        print("\n📈 YAKUNIY STATISTIKA:")
        for class_name, count in self.stats.items():
            print(f"   {class_name}: {count}")
        
        return self.stats
    
    def process_camera(self, camera_id=0):
        """
        Real-time kamera oqimini qayta ishlash
        
        Args:
            camera_id: Kamera ID (default 0)
        """
        print(f"\n📹 Kamera ishga tushmoqda (ID: {camera_id})...")
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            raise ValueError(f"❌ Kamera ochilmadi: {camera_id}")
        
        # Kamera sozlamalari
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_RESOLUTION[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_RESOLUTION[1])
        
        print("✅ Kamera tayyor!")
        print("💡 Chiqish uchun 'q' tugmasini bosing")
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Frame o'qilmadi")
                    break
                
                # Frame qayta ishlash
                processed_frame = self.process_frame(frame)
                
                # Ko'rsatish
                cv2.imshow('Object Counting System - Camera', processed_frame)
                
                # 'q' bosilsa to'xtatish
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        print("\n✅ Kamera to'xtatildi!")
        print("\n📈 YAKUNIY STATISTIKA:")
        for class_name, count in self.stats.items():
            print(f"   {class_name}: {count}")
    
    def reset_counter(self):
        """Sanagichni qayta tiklash"""
        self.counted_ids.clear()
        self.stats = {name: 0 for name in self.count_classes.values()}
        self.previous_positions.clear()
        print("🔄 Sanagich qayta tiklandi")

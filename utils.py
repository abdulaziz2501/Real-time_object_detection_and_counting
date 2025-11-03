"""
Object Counting System - Yordamchi Funksiyalar
Video ishlash, chizish va boshqa utility funksiyalar
"""

import cv2
import numpy as np
from datetime import datetime
import pandas as pd
from pathlib import Path
import config


class ObjectTracker:
    """
    Obyektlarni kuzatish va ID berish uchun klass
    Bu klass har bir obyektga unique ID beradi va ularni kuzatib boradi
    """
    
    def __init__(self, max_disappeared=50, max_distance=50):
        """
        Args:
            max_disappeared: Obyekt yo'qolganidan keyin necha frame kutish
            max_distance: Tracking uchun maksimal masofa
        """
        self.next_object_id = 0
        self.objects = {}  # ID: centroid
        self.disappeared = {}  # ID: disappeared frames soni
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
    
    def register(self, centroid):
        """Yangi obyektni ro'yxatdan o'tkazish"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
        return self.next_object_id - 1
    
    def deregister(self, object_id):
        """Obyektni ro'yxatdan o'chirish"""
        del self.objects[object_id]
        del self.disappeared[object_id]
    
    def update(self, detections):
        """
        Obyektlarni yangilash va kuzatish
        
        Args:
            detections: [(x1, y1, x2, y2, class_id, confidence), ...]
        
        Returns:
            dict: {object_id: (centroid, class_id, bbox)}
        """
        # Agar detection bo'lmasa
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            return {}
        
        # Centroidlarni hisoblash
        input_centroids = []
        input_data = []
        
        for det in detections:
            x1, y1, x2, y2, class_id, conf = det
            cx = int((x1 + x2) / 2.0)
            cy = int((y1 + y2) / 2.0)
            input_centroids.append((cx, cy))
            input_data.append((det, class_id))
        
        # Agar hech qanday obyekt kuzatilmayotgan bo'lsa
        if len(self.objects) == 0:
            result = {}
            for i, centroid in enumerate(input_centroids):
                obj_id = self.register(centroid)
                det, class_id = input_data[i]
                result[obj_id] = (centroid, class_id, det[:4])
            return result
        
        # Mavjud obyektlar bilan yangi detectionlarni matching qilish
        object_ids = list(self.objects.keys())
        object_centroids = list(self.objects.values())
        
        # Masofalarni hisoblash
        distances = []
        for obj_centroid in object_centroids:
            row = []
            for input_centroid in input_centroids:
                dist = np.sqrt(
                    (obj_centroid[0] - input_centroid[0]) ** 2 +
                    (obj_centroid[1] - input_centroid[1]) ** 2
                )
                row.append(dist)
            distances.append(row)
        
        distances = np.array(distances)
        
        # Eng yaqin juftliklarni topish
        rows = distances.min(axis=1).argsort()
        cols = distances.argmin(axis=1)[rows]
        
        used_rows = set()
        used_cols = set()
        result = {}
        
        for (row, col) in zip(rows, cols):
            if row in used_rows or col in used_cols:
                continue
            
            if distances[row, col] > self.max_distance:
                continue
            
            object_id = object_ids[row]
            self.objects[object_id] = input_centroids[col]
            self.disappeared[object_id] = 0
            
            det, class_id = input_data[col]
            result[object_id] = (input_centroids[col], class_id, det[:4])
            
            used_rows.add(row)
            used_cols.add(col)
        
        # Unused rows - disappeared obyektlar
        unused_rows = set(range(distances.shape[0])) - used_rows
        for row in unused_rows:
            object_id = object_ids[row]
            self.disappeared[object_id] += 1
            
            if self.disappeared[object_id] > self.max_disappeared:
                self.deregister(object_id)
        
        # Unused cols - yangi obyektlar
        unused_cols = set(range(distances.shape[1])) - used_cols
        for col in unused_cols:
            obj_id = self.register(input_centroids[col])
            det, class_id = input_data[col]
            result[obj_id] = (input_centroids[col], class_id, det[:4])
        
        return result


def draw_counting_line(frame, position=0.5):
    """
    Sanash chizig'ini chizish
    
    Args:
        frame: Video frame
        position: Chiziqning pozitsiyasi (0.0 - 1.0)
    
    Returns:
        tuple: (frame, line_y)
    """
    height, width = frame.shape[:2]
    line_y = int(height * position)
    
    cv2.line(frame, (0, line_y), (width, line_y), 
             config.LINE_COLOR, config.LINE_THICKNESS)
    
    # Chiziq yonida yozuv
    cv2.putText(frame, "SANASH CHIZIG'I", (10, line_y - 10),
                config.FONT, 0.7, config.LINE_COLOR, 2)
    
    return frame, line_y


def draw_detection(frame, bbox, object_id, class_name, confidence):
    """
    Obyekt atrofiga box va ma'lumotlarni chizish
    
    Args:
        frame: Video frame
        bbox: (x1, y1, x2, y2)
        object_id: Obyekt ID
        class_name: Obyekt nomi
        confidence: Ishonch darajasi
    """
    x1, y1, x2, y2 = map(int, bbox)
    
    # Box chizish
    cv2.rectangle(frame, (x1, y1), (x2, y2), config.BOX_COLOR, 2)
    
    # Label va ID
    label = f"ID:{object_id} {class_name} {confidence:.2f}"
    
    # Text background
    (text_width, text_height), baseline = cv2.getTextSize(
        label, config.FONT, config.FONT_SCALE, 1
    )
    
    cv2.rectangle(frame, (x1, y1 - text_height - 10), 
                  (x1 + text_width, y1), config.BOX_COLOR, -1)
    
    # Text
    cv2.putText(frame, label, (x1, y1 - 5),
                config.FONT, config.FONT_SCALE, config.TEXT_COLOR, 1)
    
    return frame


def draw_statistics(frame, stats):
    """
    Statistikani ekranga chizish
    
    Args:
        frame: Video frame
        stats: Statistika dict
    """
    height, width = frame.shape[:2]
    
    # Background panel
    panel_height = 150
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (400, panel_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Title
    cv2.putText(frame, "STATISTIKA", (20, 35),
                config.FONT, 0.8, (0, 255, 255), 2)
    
    # Statistikani ko'rsatish
    y_offset = 65
    for class_name, count in stats.items():
        text = f"{class_name}: {count}"
        cv2.putText(frame, text, (20, y_offset),
                    config.FONT, 0.6, (255, 255, 255), 1)
        y_offset += 25
    
    return frame


def save_statistics_to_csv(stats, filename):
    """
    Statistikani CSV faylga saqlash
    
    Args:
        stats: Statistika dictionary
        filename: Fayl nomi
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        'Timestamp': [timestamp],
        **{f'{key}': [value] for key, value in stats.items()}
    }
    
    df = pd.DataFrame(data)
    filepath = config.OUTPUT_DIR / filename
    
    # Agar fayl mavjud bo'lsa, qo'shish, aks holda yangi yaratish
    if filepath.exists():
        df.to_csv(filepath, mode='a', header=False, index=False)
    else:
        df.to_csv(filepath, index=False)
    
    print(f"✅ Statistika saqlandi: {filepath}")


def get_video_writer(input_video_path, output_video_path):
    """
    Video yozuvchi yaratish
    
    Args:
        input_video_path: Kirish video fayli
        output_video_path: Chiqish video fayli
    
    Returns:
        tuple: (VideoWriter, fps, frame_count)
    """
    cap = cv2.VideoCapture(input_video_path)
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    cap.release()
    
    return out, fps, frame_count


def format_time(seconds):
    """
    Sekundlarni soat:daqiqa:soniya formatiga o'tkazish
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

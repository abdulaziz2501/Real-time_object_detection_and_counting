"""
Object Counting System - Asosiy Dastur
Aqlli kamera tizimi: odamlar, mashinalar va boshqa obyektlarni sanash

Ishlatish:
    python app.py --video input.mp4          # Video faylni qayta ishlash
    python app.py --camera                   # Real-time kamera
    python app.py --video input.mp4 --save   # Natija videoni saqlash
"""

import argparse
import sys
from pathlib import Path
import cv2

# O'z modullarimiz
import config
from counter import ObjectCounter
from utils import save_statistics_to_csv


def parse_arguments():
    """
    Komanda qatori argumentlarini o'qish
    """
    parser = argparse.ArgumentParser(
        description='Object Counting System - Obyektlarni sanash tizimi',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Input manbalari
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '--video', '-v',
        type=str,
        help='Video fayl yo\'li'
    )
    source_group.add_argument(
        '--camera', '-c',
        action='store_true',
        help='Real-time kameradan foydalanish'
    )
    
    # Qo'shimcha parametrlar
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Chiqish video fayli nomi (default: auto)'
    )
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Natija videoni saqlash'
    )
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Ekranda ko\'rsatmaslik (faqat saqlash)'
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default=config.YOLO_MODEL,
        help=f'YOLO model fayli (default: {config.YOLO_MODEL})'
    )
    parser.add_argument(
        '--camera-id',
        type=int,
        default=0,
        help='Kamera ID (default: 0)'
    )
    parser.add_argument(
        '--confidence', '-conf',
        type=float,
        default=config.CONFIDENCE_THRESHOLD,
        help=f'Ishonch darajasi threshold (default: {config.CONFIDENCE_THRESHOLD})'
    )
    
    return parser.parse_args()


def download_yolo_model(model_name):
    """
    YOLO modelini avtomatik yuklab olish
    
    Args:
        model_name: Model nomi (masalan, 'yolov8n.pt')
    """
    from ultralytics import YOLO
    
    model_path = config.MODELS_DIR / model_name
    
    if not model_path.exists():
        print(f"📥 Model topilmadi. Yuklab olinmoqda: {model_name}")
        print("⏳ Bu biroz vaqt olishi mumkin...")
        
        try:
            # Model yuklab olish (ultralytics avtomatik download qiladi)
            model = YOLO(model_name)
            
            # Modelni to'g'ri joyga ko'chirish
            import shutil
            from pathlib import Path
            
            # Ultralytics cache papkasidan topish
            cache_dir = Path.home() / '.cache' / 'ultralytics'
            
            # Model faylini qidirish
            for file in cache_dir.rglob(model_name):
                shutil.copy(file, model_path)
                print(f"✅ Model saqlandi: {model_path}")
                break
            
        except Exception as e:
            print(f"❌ Model yuklab olishda xato: {e}")
            sys.exit(1)
    else:
        print(f"✅ Model topildi: {model_path}")


def main():
    """
    Asosiy dastur funksiyasi
    """
    print("=" * 60)
    print("🎯 OBJECT COUNTING SYSTEM - Obyektlarni Sanash Tizimi")
    print("=" * 60)
    
    # Argumentlarni o'qish
    args = parse_arguments()
    
    # Modelni yuklab olish
    download_yolo_model(args.model)
    
    # Konfiguratsiyani yangilash
    config.CONFIDENCE_THRESHOLD = args.confidence
    config.DISPLAY_OUTPUT = not args.no_display
    
    # Counter yaratish
    model_path = str(config.MODELS_DIR / args.model)
    counter = ObjectCounter(model_path=model_path)
    
    try:
        # Video rejimi
        if args.video:
            video_path = args.video
            
            # Video mavjudligini tekshirish
            if not Path(video_path).exists():
                print(f"❌ Video topilmadi: {video_path}")
                sys.exit(1)
            
            # Output fayl nomi
            output_path = None
            if args.save or args.output:
                if args.output:
                    output_name = args.output
                else:
                    input_name = Path(video_path).stem
                    output_name = f"{input_name}_counted.mp4"
                
                output_path = str(config.OUTPUT_DIR / output_name)
            
            # Videoni qayta ishlash
            stats = counter.process_video(
                video_path=video_path,
                output_path=output_path,
                display=config.DISPLAY_OUTPUT
            )
            
            # Statistikani saqlash
            if config.SAVE_STATISTICS:
                save_statistics_to_csv(stats, config.STATS_FILENAME)
        
        # Kamera rejimi
        elif args.camera:
            counter.process_camera(camera_id=args.camera_id)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Dastur to'xtatildi (Ctrl+C)")
    
    except Exception as e:
        print(f"\n❌ Xato yuz berdi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("✅ Dastur muvaffaqiyatli yakunlandi!")
    print("=" * 60)


if __name__ == "__main__":
    main()

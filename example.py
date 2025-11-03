"""
Object Counting System - Oddiy Ishlatish Namunasi
Bu fayl tizimni qanday ishlatishni ko'rsatadi
"""

from counter import ObjectCounter
import config


def example_1_video_processing():
    """
    Misol 1: Videoni qayta ishlash
    """
    print("=" * 60)
    print("MISOL 1: VIDEO QAYTA ISHLASH")
    print("=" * 60)
    
    # Counter yaratish
    counter = ObjectCounter()
    
    # Video faylni ko'rsating
    video_path = "input_videos/test.mp4"
    output_path = "output_videos/example1_result.mp4"
    
    # Qayta ishlash
    stats = counter.process_video(
        video_path=video_path,
        output_path=output_path,
        display=True  # Ekranda ko'rsatish
    )
    
    print(f"\n✅ Natija: {stats}")


def example_2_camera():
    """
    Misol 2: Real-time kamera
    """
    print("=" * 60)
    print("MISOL 2: REAL-TIME KAMERA")
    print("=" * 60)
    
    # Counter yaratish
    counter = ObjectCounter()
    
    # Kamera'ni ishga tushirish
    counter.process_camera(camera_id=0)


def example_3_custom_settings():
    """
    Misol 3: Custom sozlamalar bilan
    """
    print("=" * 60)
    print("MISOL 3: CUSTOM SOZLAMALAR")
    print("=" * 60)
    
    # Sozlamalarni o'zgartirish
    config.CONFIDENCE_THRESHOLD = 0.7  # Yuqoriroq threshold
    config.COUNTING_LINE_POSITION = 0.3  # Chiziq yuqoriroqda
    config.SKIP_FRAMES = 1  # Har bir frameni qayta ishlash
    
    # Counter yaratish
    counter = ObjectCounter()
    
    # Faqat kerakli klasslarni sanash
    custom_classes = {
        0: "Odam",      # Faqat odamlar
        2: "Mashina",   # va mashinalar
    }
    counter.count_classes = custom_classes
    counter.stats = {name: 0 for name in custom_classes.values()}
    
    # Video qayta ishlash
    video_path = "input_videos/test.mp4"
    output_path = "output_videos/example3_custom.mp4"
    
    stats = counter.process_video(
        video_path=video_path,
        output_path=output_path,
        display=True
    )
    
    print(f"\n✅ Natija: {stats}")


def example_4_multiple_videos():
    """
    Misol 4: Bir nechta videoni ketma-ket qayta ishlash
    """
    print("=" * 60)
    print("MISOL 4: KO'P VIDEOLAR")
    print("=" * 60)
    
    videos = [
        "input_videos/video1.mp4",
        "input_videos/video2.mp4",
        "input_videos/video3.mp4",
    ]
    
    counter = ObjectCounter()
    all_stats = {}
    
    for i, video_path in enumerate(videos, 1):
        print(f"\n🎥 Video {i}/{len(videos)}: {video_path}")
        
        # Har bir video uchun yangi counter (yoki reset)
        counter.reset_counter()
        
        output_path = f"output_videos/example4_video{i}.mp4"
        
        try:
            stats = counter.process_video(
                video_path=video_path,
                output_path=output_path,
                display=False  # Batch processing - ko'rsatmaslik
            )
            all_stats[video_path] = stats
        
        except Exception as e:
            print(f"❌ Xato: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("UMUMIY NATIJALAR:")
    print("=" * 60)
    for video, stats in all_stats.items():
        print(f"\n{video}:")
        for class_name, count in stats.items():
            print(f"  {class_name}: {count}")


def example_5_statistics():
    """
    Misol 5: Statistikani saqlash va tahlil qilish
    """
    print("=" * 60)
    print("MISOL 5: STATISTIKA TAHLILI")
    print("=" * 60)
    
    import pandas as pd
    from utils import save_statistics_to_csv
    
    # Video qayta ishlash
    counter = ObjectCounter()
    video_path = "input_videos/test.mp4"
    
    stats = counter.process_video(
        video_path=video_path,
        output_path=None,  # Videoni saqlamaslik
        display=False
    )
    
    # Statistikani saqlash
    save_statistics_to_csv(stats, "example5_stats.csv")
    
    # CSV ni o'qish va tahlil qilish
    csv_path = config.OUTPUT_DIR / "example5_stats.csv"
    
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        
        print("\n📊 STATISTIKA TAHLILI:")
        print("-" * 60)
        print(df)
        print("-" * 60)
        
        # Umumiy statistika
        print("\n📈 UMUMIY:")
        for col in df.columns:
            if col != 'Timestamp':
                total = df[col].sum()
                avg = df[col].mean()
                print(f"  {col}:")
                print(f"    Jami: {total}")
                print(f"    O'rtacha: {avg:.1f}")


if __name__ == "__main__":
    """
    Qaysi misol'ni ishga tushirishni tanlang
    """
    
    print("\n🎯 OBJECT COUNTING SYSTEM - MISOLLAR\n")
    print("Qaysi misol'ni ko'rmoqchisiz?")
    print("1 - Video qayta ishlash")
    print("2 - Real-time kamera")
    print("3 - Custom sozlamalar")
    print("4 - Ko'p videolar")
    print("5 - Statistika tahlili")
    print()
    
    choice = input("Tanlang (1-5): ").strip()
    
    if choice == "1":
        example_1_video_processing()
    elif choice == "2":
        example_2_camera()
    elif choice == "3":
        example_3_custom_settings()
    elif choice == "4":
        example_4_multiple_videos()
    elif choice == "5":
        example_5_statistics()
    else:
        print("❌ Noto'g'ri tanlov!")
        print("💡 Misol: python example.py")
        print("   Keyin raqam kiriting: 1")

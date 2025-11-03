#!/bin/bash

# Object Counting System - Ishga Tushirish Skripti (Linux/Mac)

echo "======================================================"
echo "🎯 Object Counting System"
echo "======================================================"

# Virtual environment'ni tekshirish
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment topilmadi!"
    echo "💡 Avval install.sh ni ishga tushiring:"
    echo "   bash install.sh"
    exit 1
fi

# Virtual environment'ni faollashtirish
source venv/bin/activate

echo ""
echo "Qanday rejimda ishlatmoqchisiz?"
echo ""
echo "1 - Kamera (real-time)"
echo "2 - Video fayl"
echo "3 - Misollar"
echo "4 - Yordam"
echo ""

read -p "Tanlang (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎥 Kamera rejimi ishga tushmoqda..."
        python app.py --camera
        ;;
    2)
        echo ""
        read -p "Video fayl yo'li: " video_path
        echo ""
        read -p "Natijani saqlashmi? (y/n): " save_choice
        
        if [ "$save_choice" = "y" ] || [ "$save_choice" = "Y" ]; then
            python app.py --video "$video_path" --save
        else
            python app.py --video "$video_path"
        fi
        ;;
    3)
        echo ""
        echo "📚 Misollar..."
        python example.py
        ;;
    4)
        echo ""
        python app.py --help
        ;;
    *)
        echo ""
        echo "❌ Noto'g'ri tanlov!"
        ;;
esac

echo ""
echo "======================================================"
echo "✅ Dastur tugadi"
echo "======================================================"

#!/bin/bash

# Object Counting System - O'rnatish Skripti (Linux/Mac)

echo "======================================================"
echo "🎯 Object Counting System - O'RNATISH"
echo "======================================================"

# Python versiyasini tekshirish
echo ""
echo "📋 Python versiyasini tekshiryapman..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python3 topilmadi!"
    echo "💡 Iltimos, Python 3.8+ versiyasini o'rnating"
    exit 1
fi

# Virtual environment yaratish
echo ""
echo "🔧 Virtual environment yaratyapman..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Virtual environment yaratilmadi!"
    echo "💡 python3-venv o'rnatilganini tekshiring"
    exit 1
fi

# Virtual environment'ni faollashtirish
echo ""
echo "⚡ Virtual environment'ni faollashtirish..."
source venv/bin/activate

# Pip'ni yangilash
echo ""
echo "📦 pip'ni yangillayapman..."
pip install --upgrade pip

# Requirements o'rnatish
echo ""
echo "📥 Kerakli kutubxonalarni o'rnatyapman..."
echo "⏳ Bu bir necha daqiqa davom etishi mumkin..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Kutubxonalar o'rnatilmadi!"
    exit 1
fi

# .env fayl yaratish
echo ""
echo "⚙️  .env fayl yaratyapman..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env fayli yaratildi"
else
    echo "ℹ️  .env fayli allaqachon mavjud"
fi

# Papkalarni tekshirish
echo ""
echo "📁 Papkalarni tekshiryapman..."
mkdir -p models input_videos output_videos

echo ""
echo "======================================================"
echo "✅ O'RNATISH MUVAFFAQIYATLI YAKUNLANDI!"
echo "======================================================"
echo ""
echo "📝 KEYINGI QADAMLAR:"
echo ""
echo "1. Virtual environment'ni faollashtiring:"
echo "   source venv/bin/activate"
echo ""
echo "2. Dasturni ishga tushiring:"
echo "   python app.py --camera"
echo "   yoki"
echo "   python app.py --video input_videos/test.mp4 --save"
echo ""
echo "3. Yordamni ko'rish:"
echo "   python app.py --help"
echo ""
echo "4. Misollarni ko'rish:"
echo "   python example.py"
echo ""
echo "======================================================"

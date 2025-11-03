@echo off
REM Object Counting System - O'rnatish Skripti (Windows)

echo ======================================================
echo 🎯 Object Counting System - O'RNATISH
echo ======================================================

REM Python versiyasini tekshirish
echo.
echo 📋 Python versiyasini tekshiryapman...
python --version

if errorlevel 1 (
    echo ❌ Python topilmadi!
    echo 💡 Iltimos, Python 3.8+ versiyasini o'rnating
    echo    python.org dan yuklab oling
    pause
    exit /b 1
)

REM Virtual environment yaratish
echo.
echo 🔧 Virtual environment yaratyapman...
python -m venv venv

if errorlevel 1 (
    echo ❌ Virtual environment yaratilmadi!
    pause
    exit /b 1
)

REM Virtual environment'ni faollashtirish
echo.
echo ⚡ Virtual environment'ni faollashtirish...
call venv\Scripts\activate.bat

REM Pip'ni yangilash
echo.
echo 📦 pip'ni yangillayapman...
python -m pip install --upgrade pip

REM Requirements o'rnatish
echo.
echo 📥 Kerakli kutubxonalarni o'rnatyapman...
echo ⏳ Bu bir necha daqiqa davom etishi mumkin...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Kutubxonalar o'rnatilmadi!
    pause
    exit /b 1
)

REM .env fayl yaratish
echo.
echo ⚙️  .env fayl yaratyapman...
if not exist .env (
    copy .env.example .env
    echo ✅ .env fayli yaratildi
) else (
    echo ℹ️  .env fayli allaqachon mavjud
)

REM Papkalarni tekshirish
echo.
echo 📁 Papkalarni tekshiryapman...
if not exist models mkdir models
if not exist input_videos mkdir input_videos
if not exist output_videos mkdir output_videos

echo.
echo ======================================================
echo ✅ O'RNATISH MUVAFFAQIYATLI YAKUNLANDI!
echo ======================================================
echo.
echo 📝 KEYINGI QADAMLAR:
echo.
echo 1. Virtual environment'ni faollashtiring:
echo    venv\Scripts\activate
echo.
echo 2. Dasturni ishga tushiring:
echo    python app.py --camera
echo    yoki
echo    python app.py --video input_videos\test.mp4 --save
echo.
echo 3. Yordamni ko'rish:
echo    python app.py --help
echo.
echo 4. Misollarni ko'rish:
echo    python example.py
echo.
echo ======================================================
pause

@echo off
REM Object Counting System - Ishga Tushirish Skripti (Windows)

echo ======================================================
echo 🎯 Object Counting System
echo ======================================================

REM Virtual environment'ni tekshirish
if not exist venv (
    echo ❌ Virtual environment topilmadi!
    echo 💡 Avval install.bat ni ishga tushiring
    pause
    exit /b 1
)

REM Virtual environment'ni faollashtirish
call venv\Scripts\activate.bat

echo.
echo Qanday rejimda ishlatmoqchisiz?
echo.
echo 1 - Kamera (real-time)
echo 2 - Video fayl
echo 3 - Misollar
echo 4 - Yordam
echo.

set /p choice="Tanlang (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🎥 Kamera rejimi ishga tushmoqda...
    python app.py --camera
    
) else if "%choice%"=="2" (
    echo.
    set /p video_path="Video fayl yo'li: "
    echo.
    set /p save_choice="Natijani saqlashmi? (y/n): "
    
    if /i "%save_choice%"=="y" (
        python app.py --video "%video_path%" --save
    ) else (
        python app.py --video "%video_path%"
    )
    
) else if "%choice%"=="3" (
    echo.
    echo 📚 Misollar...
    python example.py
    
) else if "%choice%"=="4" (
    echo.
    python app.py --help
    
) else (
    echo.
    echo ❌ Noto'g'ri tanlov!
)

echo.
echo ======================================================
echo ✅ Dastur tugadi
echo ======================================================
pause

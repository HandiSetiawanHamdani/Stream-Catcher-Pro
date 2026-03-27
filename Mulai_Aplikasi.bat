@echo off
:: Mengunci lokasi folder ke tempat file ini berada
cd /d "%~dp0"

title LiveRecorder Studio - Server
color 0b
echo ===================================================
echo [INFO] Menyalakan Server Recorder Pro...
:: Simbol pipe (|) diganti dengan strip (-) agar tidak error
echo [INFO] Laptop: Acer Aspire 3 - RAM 4GB
echo [INFO] Status: Auto-Import Brave Aktif
echo ===================================================
echo.

:: Mengaktifkan Virtual Environment
call venv\Scripts\activate

:: Menjalankan Streamlit
streamlit run app.py --browser.gatherUsageStats false

pause
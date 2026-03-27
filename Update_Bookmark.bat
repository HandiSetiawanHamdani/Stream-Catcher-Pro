@echo off
:: Mengunci lokasi folder ke tempat file ini berada
cd /d "%~dp0"

title Manual Bookmark Sync
color 0a
echo ===================================================
echo [INFO] Sinkronisasi Manual Bookmark 'bg' Brave... [cite: 3]
echo ===================================================
echo.

call venv\Scripts\activate
python import_brave.py

echo.
echo [SUKSES] Database hosts_data.json telah diperbarui. [cite: 4]
echo.
pause
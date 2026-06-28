@echo off
title Inventario y Caja
cd /d "%~dp0"

echo Iniciando el sistema de Inventario y Caja...
echo No cierres esta ventana mientras uses el programa.
echo.

start "" "http://127.0.0.1:5000"

".\venv\Scripts\python.exe" app.py

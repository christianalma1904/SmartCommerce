@echo off
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo No se detecto Python. Instala Python 3.10 o superior y agregalo al PATH.
  pause
  exit /b 1
)
echo SmartCommerce - abre http://127.0.0.1:8000 en tu navegador.
python backend\servidor.py
pause

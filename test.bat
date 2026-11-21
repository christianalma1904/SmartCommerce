@echo off
cd /d "%~dp0"
python -m unittest discover -s backend\tests -p "test_*.py" -v
pause

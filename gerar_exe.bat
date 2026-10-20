@echo off
cd /d "%~dp0"
echo Instalando dependencias...
python -m pip install -r requirements.txt pyinstaller
echo.
echo Gerando o executavel (pode demorar alguns minutos)...
python -m PyInstaller --noconfirm --clean --windowed ^
  --name Transcritor ^
  --version-file version_info.txt ^
  --collect-all customtkinter ^
  --collect-all faster_whisper ^
  --collect-all ctranslate2 ^
  --collect-all onnxruntime ^
  --collect-all av ^
  transcrever.py
echo.
echo Pronto! O programa esta em dist\Transcritor\Transcritor.exe
pause

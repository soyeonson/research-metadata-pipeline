@echo off
setlocal
call .venv\Scripts\activate.bat
python -m unittest discover -s tests -v
endlocal

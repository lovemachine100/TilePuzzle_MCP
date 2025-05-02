@echo off
echo タイルスライドパズル MCP サーバーを起動しています...

REM 仮想環境を有効化
call venv\Scripts\activate

REM サーバーを起動
python slidepuzzle.py

pause

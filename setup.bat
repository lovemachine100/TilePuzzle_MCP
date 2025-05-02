@echo off
echo タイルスライドパズル MCP サーバー セットアップ

REM 仮想環境の作成
echo 仮想環境を作成しています...
python -m venv venv
call venv\Scripts\activate

REM 依存パッケージのインストール
echo 依存パッケージをインストールしています...
pip install -r requirements.txt

echo セットアップが完了しました！
echo サーバーを起動するには以下のコマンドを実行してください：
echo call venv\Scripts\activate
echo python slidepuzzle.py

pause

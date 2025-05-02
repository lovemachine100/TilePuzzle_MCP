# タイルスライドパズル MCP サーバー

Model Context Protocol (MCP) を活用したタイルスライドパズル（8パズル）のサーバーです。このMCPサーバーを使用することで、AIエージェント（Claude）がパズルゲームを操作できるようになります。

## 概要

タイルスライドパズル（8パズル）は、3x3のグリッド上に配置された8つの数字タイル（1〜8）と1つの空きスペースからなるパズルです。プレイヤーは、空きスペースに隣接するタイルをスライドさせることで、数字を特定の順序（1から8まで順番に並ぶ状態）に並べ替えることを目指します。

このMCPサーバーは、パズルの状態を管理し、タイルの移動や状態の取得などの操作をAIエージェントに提供します。

## 機能

このMCPサーバーは以下の機能を提供します：

1. ゲームの初期化（難易度設定可能）
2. 現在のゲーム状態の取得
3. タイルの移動（上下左右）
4. ヒントの提供
5. ゴール状態の表示

## 環境構築

以下のコマンドで開発環境を構築します：

```bash
# プロジェクトディレクトリの作成
mkdir TilePuzzle_MCP
cd TilePuzzle_MCP

# 仮想環境の作成と有効化（Pythonの場合）
python -m venv venv
venv\Scripts\activate  # Windowsの場合

# 依存パッケージのインストール
pip install mcp[cli] numpy

# サーバースクリプトファイルの作成
# slidepuzzle.py を作成して、コードを記述
```

## サーバーの起動

作成したサーバーは以下のコマンドで起動します：

```bash
python slidepuzzle.py
```

## Claude Desktop との連携設定

Claude Desktop と連携するには、Claude Desktopの設定ファイルに以下のような設定を追加します：

```json
{
  "mcpServers": {
    "tilepuzzle": {
      "command": "python",
      "args": [
        "C:/path/to/your/TilePuzzle_MCP/slidepuzzle.py"
      ]
    }
  }
}
```

`C:/path/to/your/TilePuzzle_MCP` の部分は、実際のプロジェクトディレクトリのパスに置き換えてください。

## 使い方

このMCPサーバーが正しく設定されると、Claude Desktop から以下のツールが利用可能になります：

1. `initialize_game` - 難易度を指定してゲームを初期化する
2. `get_game_state` - 現在のゲーム状態を取得する
3. `move_tile` - タイルを指定した方向にスライドさせる
4. `get_hint` - 次の手のヒントを取得する
5. `solve_puzzle` - ゴール状態を表示する（教育目的）

### 使用例：

Claude との会話で以下のようにゲームを進めることができます：

1. まず `initialize_game` を実行してゲームを開始します（難易度は "easy", "medium", "hard" から選択）
2. `get_game_state` でゲームの現在の状態を確認します
3. `move_tile` で数字タイルを動かします（方向は0=上, 1=下, 2=左, 3=右）
4. ヒントが欲しい場合は `get_hint` を実行します
5. ゴール状態を確認したい場合は `solve_puzzle` を実行します

## 技術詳細

このMCPサーバーは以下の技術を使用しています：

- Python 3.x
- NumPy: 行列操作のためのライブラリ
- MCP SDK: Model Context Protocol の実装
- FastMCP: MCPサーバーを簡単に作成するためのフレームワーク

## 拡張アイデア

このシンプルなMCPサーバーは、以下のように拡張することができます：

1. 盤面サイズのカスタマイズ（4x4、5x5など）
2. 複数のパズルタイプ対応（数字、画像パズルなど）
3. 自動解決アルゴリズムの実装（A*アルゴリズムなど）
4. 移動履歴と元に戻す機能
5. タイムアタックモードやスコアシステム

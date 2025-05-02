import random
import numpy as np
from typing import Dict, Any, List, Tuple
from mcp.server.fastmcp import FastMCP

# FastMCP サーバーの初期化
mcp = FastMCP("tilepuzzle")

class TileSlidePuzzleEnv:
    def __init__(self, size=3):
        self.size = size
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.reset()
    
    def reset(self, shuffle_moves=50):
        # ゴール状態を設定
        self.board = np.arange(self.size**2).reshape(self.size, self.size)
        
        # 一定回数のランダムな動きでタイルを混ぜる
        for _ in range(shuffle_moves):
            action = np.random.choice(4)  # 0=上, 1=下, 2=左, 3=右
            self.slide_tile(action)
        
        return self.get_state()
    
    def get_state(self):
        """ゲームの現在の状態を取得"""
        return self.board.copy()
    
    def slide_tile(self, direction):
        """タイルをスライドさせる
        
        Args:
            direction: 0=上, 1=下, 2=左, 3=右
        
        Returns:
            bool: 移動が成功したかどうか
        """
        # 空白タイル(0)の位置を見つける
        x, y = np.where(self.board == 0)
        x, y = int(x), int(y)
        
        moved = False
        
        if direction == 0 and x < self.size - 1:  # 上
            self.board[x, y], self.board[x+1, y] = self.board[x+1, y], self.board[x, y]
            moved = True
        elif direction == 1 and x > 0:  # 下
            self.board[x, y], self.board[x-1, y] = self.board[x-1, y], self.board[x, y]
            moved = True
        elif direction == 2 and y < self.size - 1:  # 左
            self.board[x, y], self.board[x, y+1] = self.board[x, y+1], self.board[x, y]
            moved = True
        elif direction == 3 and y > 0:  # 右
            self.board[x, y], self.board[x, y-1] = self.board[x, y-1], self.board[x, y]
            moved = True
        
        return moved
    
    def is_solved(self):
        """パズルが解かれたかどうかをチェック"""
        return np.array_equal(self.board, np.arange(self.size**2).reshape(self.size, self.size))
    
    def get_valid_moves(self):
        """現在の状態で可能な移動を取得"""
        valid_moves = []
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        
        # 空白タイル(0)の位置を見つける
        x, y = np.where(self.board == 0)
        x, y = int(x), int(y)
        
        # 可能な移動を確認
        if x < self.size - 1:  # 上方向へのスライドが可能
            valid_moves.append(0)
        if x > 0:  # 下方向へのスライドが可能
            valid_moves.append(1)
        if y < self.size - 1:  # 左方向へのスライドが可能
            valid_moves.append(2)
        if y > 0:  # 右方向へのスライドが可能
            valid_moves.append(3)
        
        # 方向名と番号のペアをリストで返す
        return [(i, directions[i]) for i in valid_moves]
    
    def get_manhattan_distance(self):
        """現在の状態からゴール状態までのマンハッタン距離の合計を計算"""
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i, j]
                if value != 0:  # 空白タイルはスキップ
                    # 正しい位置を計算
                    goal_i, goal_j = value // self.size, value % self.size
                    # マンハッタン距離を加算
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

# ゲーム環境のインスタンスを作成
game = TileSlidePuzzleEnv()

# ゲームが初期化済みかどうかのフラグ
game_initialized = False

@mcp.tool()
async def initialize_game(difficulty: str = "medium") -> str:
    """タイルスライドパズルゲームを初期化する
    
    Args:
        difficulty: 難易度 ("easy", "medium", "hard")
    """
    global game_initialized
    
    shuffle_moves = 30  # デフォルト値（中級）
    
    if difficulty.lower() == "easy":
        shuffle_moves = 10
    elif difficulty.lower() == "medium":
        shuffle_moves = 30
    elif difficulty.lower() == "hard":
        shuffle_moves = 50
    else:
        return f"無効な難易度: {difficulty}。'easy', 'medium', 'hard' のいずれかを指定してください。"
    
    game.reset(shuffle_moves)
    game_initialized = True
    
    return f"{difficulty} 難易度でゲームを初期化しました。\n{format_board(game.get_state())}"

@mcp.tool()
async def get_game_state() -> str:
    """現在のゲーム状態を取得する"""
    global game_initialized
    
    if not game_initialized:
        return "ゲームがまだ初期化されていません。initialize_game を実行してください。"
    
    state = game.get_state()
    
    is_solved = game.is_solved()
    valid_moves = game.get_valid_moves()
    manhattan_distance = game.get_manhattan_distance()
    
    result = f"現在のボード状態:\n{format_board(state)}\n\n"
    result += f"ゲームクリア: {'はい' if is_solved else 'いいえ'}\n"
    result += f"マンハッタン距離（ゴールまでの距離の目安）: {manhattan_distance}\n"
    result += "有効な移動: " + ", ".join([f"{name}({i})" for i, name in valid_moves])
    
    return result

@mcp.tool()
async def move_tile(direction: int) -> str:
    """タイルを指定した方向にスライドさせる
    
    Args:
        direction: 移動方向 (0=上, 1=下, 2=左, 3=右)
    """
    global game_initialized
    
    if not game_initialized:
        return "ゲームがまだ初期化されていません。initialize_game を実行してください。"
    
    direction_names = ["上", "下", "左", "右"]
    
    if not 0 <= direction <= 3:
        return f"無効な方向: {direction}。0（上）、1（下）、2（左）、3（右）のいずれかを指定してください。"
    
    moved = game.slide_tile(direction)
    
    if not moved:
        return f"{direction_names[direction]}方向への移動はできません。"
    
    state = game.get_state()
    is_solved = game.is_solved()
    
    result = f"{direction_names[direction]}方向に移動しました。\n\n{format_board(state)}\n\n"
    
    if is_solved:
        result += "おめでとうございます！パズルを解きました！"
    
    return result

@mcp.tool()
async def get_hint() -> str:
    """次の手のヒントを取得する"""
    global game_initialized
    
    if not game_initialized:
        return "ゲームがまだ初期化されていません。initialize_game を実行してください。"
    
    if game.is_solved():
        return "パズルはすでに解かれています。"
    
    # マンハッタン距離に基づく簡単なヒント
    current_distance = game.get_manhattan_distance()
    best_move = None
    best_distance = float('inf')
    direction_names = ["上", "下", "左", "右"]
    
    # 可能な各移動を試し、最もマンハッタン距離が減少する移動を見つける
    for direction, _ in game.get_valid_moves():
        # 現在の状態を保存
        temp_board = game.board.copy()
        
        # 移動を試す
        game.slide_tile(direction)
        
        # 移動後のマンハッタン距離を計算
        new_distance = game.get_manhattan_distance()
        
        # より良い移動を見つけた場合、それを保存
        if new_distance < best_distance:
            best_distance = new_distance
            best_move = direction
        
        # 状態を元に戻す
        game.board = temp_board
    
    if best_move is not None and best_distance < current_distance:
        return f"ヒント: {direction_names[best_move]}方向（{best_move}）に移動することで、ゴールに近づきます。"
    else:
        return "ヒント: 複数の移動が必要です。次の数手先を考えてみてください。"

@mcp.tool()
async def solve_puzzle() -> str:
    """パズルをリセットして解く（教育目的）"""
    global game_initialized
    
    if not game_initialized:
        return "ゲームがまだ初期化されていません。initialize_game を実行してください。"
    
    # 現在の状態を保存
    original_state = game.board.copy()
    
    # ゴール状態にリセット
    game.board = np.arange(game.size**2).reshape(game.size, game.size)
    
    result = "パズルは以下のようにゴール状態になります：\n\n"
    result += format_board(game.get_state())
    
    # 状態を元に戻す
    game.board = original_state
    
    return result

def format_board(board):
    """ボードを読みやすい形式にフォーマット"""
    result = ""
    for row in board:
        row_str = " | ".join([str(cell) if cell != 0 else " " for cell in row])
        result += f"| {row_str} |\n"
    return result

if __name__ == "__main__":
    # サーバーの初期化と実行
    mcp.run(transport='stdio')

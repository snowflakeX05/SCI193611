from games import Game, GameState, alpha_beta_player

class Hexapawn(Game):
    def __init__(self, size=3):
        self.size = size
        board = tuple(
            tuple(['B'] * size) if r == 0 else
            tuple(['W'] * size) if r == size - 1 else
            tuple(['.'] * size)
            for r in range(size)
        )
        self.initial = GameState(to_move='W', utility=0, board=board, moves=self.get_moves(board, 'W'))

    def get_moves(self, board, player):
        moves = []
        direction = -1 if player == 'W' else 1
        enemy = 'B' if player == 'W' else 'W'
        
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == player:
                    nr = r + direction
                    if 0 <= nr < self.size:
                        if board[nr][c] == '.':
                            moves.append(((r, c), (nr, c)))
                        if c - 1 >= 0 and board[nr][c-1] == enemy:
                            moves.append(((r, c), (nr, c-1)))
                        if c + 1 < self.size and board[nr][c+1] == enemy:
                            moves.append(((r, c), (nr, c+1)))
        return moves

    def actions(self, state):
        return self.get_moves(state.board, state.to_move)

    def result(self, state, move):
        if move not in self.actions(state):
            return state
            
        board = [list(row) for row in state.board]
        (r, c), (nr, nc) = move
        player = state.to_move
        
        board[nr][nc] = player
        board[r][c] = '.'
        
        new_board = tuple(tuple(row) for row in board)
        next_player = 'B' if player == 'W' else 'W'
        util = self.compute_utility(new_board, player, next_player)
        
        return GameState(to_move=next_player, utility=util, board=new_board, moves=self.get_moves(new_board, next_player))

    def utility(self, state, player):
        return state.utility if player == 'W' else -state.utility

    def terminal_test(self, state):
        return state.utility != 0 or len(self.actions(state)) == 0

    def compute_utility(self, board, last_player, next_player):
        if last_player == 'W' and 'W' in board[0]: return 1
        if last_player == 'B' and 'B' in board[self.size - 1]: return -1
        if not any('W' in row for row in board): return -1
        if not any('B' in row for row in board): return 1
        if not self.get_moves(board, next_player): return 1 if last_player == 'W' else -1
        return 0

    def display(self, state):
        print("\n    0   1   2")
        print("  -------------")
        for i, row in enumerate(state.board):
            print(f"{i} | " + " | ".join(row) + " |")
            print("  -------------")
        print(f"คิวเดินต่อไป: {state.to_move}\n")


def human_player(game, state):
    """ฟังก์ชันสำหรับให้ผู้เล่นป้อนคำสั่งผ่าน Console ได้ง่ายๆ"""
    legal_moves = game.actions(state)
    print("ตาเดินที่เป็นไปได้:")
    for i, move in enumerate(legal_moves):
        (r, c), (nr, nc) = move
        print(f"  [{i}] จาก ({r},{c}) ไป ({nr},{nc})")
        
    while True:
        try:
            choice = int(input(f"เลือกหมายเลขตาเดิน [0-{len(legal_moves)-1}]: "))
            if 0 <= choice < len(legal_moves):
                return legal_moves[choice]
            print("❌ หมายเลขไม่อยู่ในตัวเลือก ลองใหม่")
        except ValueError:
            print("❌ กรุณาพิมพ์ตัวเลขเท่านั้น")


if __name__ == "__main__":
    game = Hexapawn()
    print("="*35)
    print("  🔥 HEXAPAWN vs AlphaBeta AI 🔥")
    print("="*35)
    print("ผู้เล่น = 'W' (White) | เริ่มก่อน เดินขึ้น")
    print("AI   = 'B' (Black) | เดินลง")

    result = game.play_game(human_player, alpha_beta_player)
    
    print("="*35)
    if result == 1:
        print("🎉🎉 ยินดีด้วย! White เป็นผู้ชนะ 🎉🎉")
    elif result == -1:
        print("💀💀 Black (AI) เป็นผู้ชนะ 💀💀")
    else:
        print("🤝 เสมอ!")
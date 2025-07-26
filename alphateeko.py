import random
import time
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['X', 'O']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.AI_SEARCH_DEPTH = 3 # The depth for the minimax search

    def heuristic_game_value(self, state, piece):
        """
        Calculates a heuristic value for a non-terminal game state.
        A higher positive value is better for the AI, a lower negative value is better for the opponent.
        The heuristic prioritizes having more pieces in a line or box formation.
        """
        my_val = 0
        opp_val = 0

        # Check all possible winning lines for my piece and opponent's piece
        for i in range(5):
            for j in range(5):
                # Horizontal
                if j <= 1:
                    my_val = max(my_val, self._count_line(state, i, j, 0, 1, self.my_piece))
                    opp_val = max(opp_val, self._count_line(state, i, j, 0, 1, self.opp))
                # Vertical
                if i <= 1:
                    my_val = max(my_val, self._count_line(state, i, j, 1, 0, self.my_piece))
                    opp_val = max(opp_val, self._count_line(state, i, j, 1, 0, self.opp))
                # Diagonal (top-left to bottom-right)
                if i <= 1 and j <= 1:
                    my_val = max(my_val, self._count_line(state, i, j, 1, 1, self.my_piece))
                    opp_val = max(opp_val, self._count_line(state, i, j, 1, 1, self.opp))
                # Diagonal (top-right to bottom-left)
                if i <= 1 and j >= 3:
                    my_val = max(my_val, self._count_line(state, i, j, 1, -1, self.my_piece))
                    opp_val = max(opp_val, self._count_line(state, i, j, 1, -1, self.opp))
                # 2x2 Box
                if i < 4 and j < 4:
                    my_val = max(my_val, self._count_box(state, i, j, self.my_piece))
                    opp_val = max(opp_val, self._count_box(state, i, j, self.opp))

        return (my_val - opp_val) / 4 # Normalize to be between -1 and 1

    def _count_line(self, state, r, c, dr, dc, piece):
        """ Helper to count pieces in a line of 4 for the heuristic. """
        count = 0
        for i in range(4):
            if state[r + i*dr][c + i*dc] == piece:
                count += 1
            elif state[r + i*dr][c + i*dc] != ' ':
                return 0 # Blocked by opponent
        return count

    def _count_box(self, state, r, c, piece):
        """ Helper to count pieces in a 2x2 box for the heuristic. """
        count = 0
        for i in range(2):
            for j in range(2):
                if state[r+i][c+j] == piece:
                    count += 1
                elif state[r+i][c+j] != ' ':
                    return 0 # Blocked by opponent
        return count


    def _minimax(self, state, depth, is_maximizing_player):
        """
        Recursive minimax function.
        Returns a tuple of (heuristic_score, best_move)
        """
        # Check for terminal state or max depth
        game_val = self.game_value(state)
        if game_val != 0:
            return game_val, None
        if depth == self.AI_SEARCH_DEPTH:
            return self.heuristic_game_value(state, self.my_piece), None

        # Generate successors
        successors = self._generate_successors(state, self.my_piece if is_maximizing_player else self.opp)

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for succ_state, move in successors:
                evaluation, _ = self._minimax(succ_state, depth + 1, False)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
            return max_eval, best_move
        else: # Minimizing player
            min_eval = float('inf')
            best_move = None
            for succ_state, move in successors:
                evaluation, _ = self._minimax(succ_state, depth + 1, True)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
            return min_eval, best_move

    def make_move(self, state):
        """ Selects a (row, col) space for the next move.

        Args:
            state (list of lists): current state of the game.

        Return:
            move (list): a list of move tuples, e.g. [(row, col)] or [(row, col), (source_row, source_col)]
        """
        # Ensure we don't modify the original state
        state_copy = copy.deepcopy(state)
        
        _, best_move = self._minimax(state_copy, 0, True)
        
        # If minimax fails to find a move (should not happen in a valid game state), pick a random one.
        if best_move is None:
            drop_phase = sum(row.count(self.my_piece) + row.count(self.opp) for row in state) < 8
            successors = self._generate_successors(state, self.my_piece)
            if successors:
                _, best_move = random.choice(successors)
            else: # No possible moves, should indicate a draw or loss
                return [] 

        return best_move


    def _generate_successors(self, state, piece):
        """Generates all possible successor states and their associated moves.

        Args:
            state (list of lists): the current game state.
            piece (str): the piece to move ('b' or 'r').

        Returns:
            list: a list of tuples (successor_state, move)
        """
        succs = []
        num_pieces = sum(row.count(self.my_piece) + row.count(self.opp) for row in state)
        drop_phase = num_pieces < 8

        if drop_phase:
            # Drop Phase: place a piece in any empty cell
            for r in range(5):
                for c in range(5):
                    if state[r][c] == ' ':
                        state_new = copy.deepcopy(state)
                        state_new[r][c] = piece
                        succs.append((state_new, [(r, c)]))
        else:
            # Move Phase: move one of your pieces to an adjacent empty cell
            for r in range(5):
                for c in range(5):
                    if state[r][c] == piece:
                        # Check all 8 adjacent cells
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                
                                r_new, c_new = r + dr, c + dc
                                
                                if 0 <= r_new < 5 and 0 <= c_new < 5 and state[r_new][c_new] == ' ':
                                    state_new = copy.deepcopy(state)
                                    state_new[r][c] = ' '
                                    state_new[r_new][c_new] = piece
                                    succs.append((state_new, [(r_new, c_new), (r, c)]))
        return succs

    def opponent_move(self, move):
        """ Validates and applies the opponent's move to the internal board state.

        Args:
            move (list): a list of move tuples.

        Raises:
            ValueError: if the move is illegal.
        """
        # Validate input format
        if not (1 <= len(move) <= 2):
            raise ValueError("Invalid move format. Move should have 1 or 2 tuples.")

        dest_r, dest_c = move[0]

        if not (0 <= dest_r < 5 and 0 <= dest_c < 5):
            raise ValueError("Move is outside the board.")

        if self.board[dest_r][dest_c] != ' ':
            raise ValueError("Illegal move: destination is already occupied.")

        # Handle move phase logic
        if len(move) > 1:
            src_r, src_c = move[1]
            if not (0 <= src_r < 5 and 0 <= src_c < 5):
                raise ValueError("Source of move is outside the board.")
            if self.board[src_r][src_c] != self.opp:
                raise ValueError(f"You don't have a piece at the source location ({chr(ord('A')+src_c)}{src_r}).")
            if abs(src_r - dest_r) > 1 or abs(src_c - dest_c) > 1:
                raise ValueError('Illegal move: can only move to an adjacent space.')
        
        # Apply the move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece. """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board. """
        print("    A   B   C   D   E")
        print("  +---+---+---+---+---+")
        for i, row in enumerate(self.board):
            print(f"{i} | {' | '.join(row)} |")
            if i < 4:
                print("  +---+---+---+---+---+")
        print("  +---+---+---+---+---+")


    def game_value(self, state):
        """ Checks the current board status for a win condition.

        Args:
            state (list of lists): the game state to check.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner.
        """
        # Check horizontal
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i] == self.my_piece else -1

        # Check vertical
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # Check \ diagonal
        for i in range(2):
            for j in range(2):
                if state[i][j]!=' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # Check / diagonal
        for i in range(2):
            for j in range(3, 5):
                if state[i][j]!=' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # Check 2x2 box
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and \
                   state[i][j] == state[i+1][j] and \
                   state[i][j] == state[i][j+1] and \
                   state[i][j] == state[i+1][j+1]:
                    return 1 if state[i][j] == self.my_piece else -1
        
        return 0 # No winner

def print_instructions():
    """Prints the game instructions."""
    print("""
    Welcome to Teeko!
    
    RULES:
    1. The game is played on a 5x5 board.
    2. Each player has four pieces ('b' for black, 'r' for red).
    3. The game has two phases: Drop Phase and Move Phase.
    
    DROP PHASE:
    - Players take turns placing one of their pieces on any empty square.
    - This continues until all 8 pieces are on the board.
    
    MOVE PHASE:
    - After the Drop Phase, players take turns moving one of their pieces to an
      adjacent empty square (horizontally, vertically, or diagonally).
      
    HOW TO WIN:
    - Get four of your pieces in a row (horizontally, vertically, or diagonally).
    - Get four of your pieces in a 2x2 square.
    
    HOW TO ENTER MOVES:
    - Use column-row format (e.g., 'A0', 'C4'). The input is not case-sensitive.
    - During the Move Phase, you will be prompted for a 'from' and 'to' location.
    """)

def get_human_move(player, is_drop_phase):
    """Gets and validates a move from the human player."""
    while True:
        try:
            if is_drop_phase:
                move_str = input(f"Enter your move (e.g., B3): ").upper()
                if len(move_str) != 2 or not ('A' <= move_str[0] <= 'E') or not ('0' <= move_str[1] <= '4'):
                    print("Invalid format. Please use column-row format (e.g., 'B3').")
                    continue
                
                col = ord(move_str[0]) - ord('A')
                row = int(move_str[1])
                move = [(row, col)]
                # Temporarily place piece to validate, then remove
                if player.board[row][col] != ' ':
                    print("That space is already occupied. Try again.")
                    continue
                return move

            else: # Move phase
                move_from_str = input("Move piece from (e.g., B3): ").upper()
                if len(move_from_str) != 2 or not ('A' <= move_from_str[0] <= 'E') or not ('0' <= move_from_str[1] <= '4'):
                    print("Invalid format for 'from' location.")
                    continue
                
                move_to_str = input("Move piece to (e.g., C4): ").upper()
                if len(move_to_str) != 2 or not ('A' <= move_to_str[0] <= 'E') or not ('0' <= move_to_str[1] <= '4'):
                    print("Invalid format for 'to' location.")
                    continue

                from_col = ord(move_from_str[0]) - ord('A')
                from_row = int(move_from_str[1])
                to_col = ord(move_to_str[0]) - ord('A')
                to_row = int(move_to_str[1])
                
                move = [(to_row, to_col), (from_row, from_col)]
                # The opponent_move function will handle detailed validation
                return move

        except (ValueError, IndexError):
            print("Invalid input. Please use the format 'A0', 'B1', etc.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    """Main game loop."""
    
    print("Welcome to AlphaTeeko, the AI for the game Teeko!")
    
    while True:
        show_help = input("Would you like to see the instructions? (yes/no): ").lower()
        if show_help in ['y', 'yes']:
            print_instructions()
            break
        elif show_help in ['n', 'no']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    ai = TeekoPlayer()
    print(f"\nYou will be playing as '{ai.opp}'. The AI is '{ai.my_piece}'.")
    
    piece_count = 0
    turn = 0 # 0 for 'b', 1 for 'r'

    # Main game loop
    while ai.game_value(ai.board) == 0:
        is_drop_phase = piece_count < 8
        current_player_piece = ai.pieces[turn]
        
        ai.print_board()

        if ai.my_piece == current_player_piece:
            # AI's turn
            print(f"\nAI's turn ({ai.my_piece})...")
            start_time = time.time()
            move = ai.make_move(ai.board)
            end_time = time.time()
            
            if not move:
                print("AI cannot make a move. It might be a draw!")
                break

            ai.place_piece(move, ai.my_piece)
            
            if is_drop_phase:
                print(f"AI placed a piece at {chr(move[0][1] + ord('A'))}{move[0][0]}")
            else:
                print(f"AI moved from {chr(move[1][1] + ord('A'))}{move[1][0]} to {chr(move[0][1] + ord('A'))}{move[0][0]}")
            print(f"(Thinking time: {end_time - start_time:.2f}s)")

        else:
            # Human's turn
            print(f"\nYour turn ({ai.opp}).")
            move_made = False
            while not move_made:
                human_move = get_human_move(ai, is_drop_phase)
                try:
                    ai.opponent_move(human_move)
                    move_made = True
                except ValueError as e:
                    print(f"Error: {e}. Please try again.")
        
        if is_drop_phase:
            piece_count += 1
            
        turn = 1 - turn # Switch turns

    # Game over
    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("\nAI wins! Game over.")
    elif ai.game_value(ai.board) == -1:
        print("\nCongratulations, you win! Game over.")
    else:
        print("\nIt's a draw! Game over.")

if __name__ == "__main__":
    main()

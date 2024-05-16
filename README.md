# Chess Prototype

Simple python implementation of chess. Created to determine the logic required for creating the game of chess.

### Notes for Implementation

- show_moves only shows the valid moves while show_attack shows the squares that the unit can attack
    - this is important for checking for valid moves for the king, since the king cannot move into squares that are being attacked(i.e. pawn movement, attacking a unit being guarded)
    - show_attack should not access the game board, since pieces with variable movement will need to use the function with a future version of the board to check for forks
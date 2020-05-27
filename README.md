# EverChess
A version of pawn only chess

Rules:
* White moves first
* Pawns can move forward one space to an empty location, or diagonally one space to capture an opponent’s pawn at that location
* A player must capture an opponent’s pawn if a capturing move is available
* On any capturing move, the player immediately moves again with another pawn that has not yet moved that turn
* The first player to get a pawn to the opposite end of the board wins, unless a player is left without any move, in which case the other player immediately wins

To play, simply run the python script:
`$ python3 EverChess.py`

Enter board locations with any of these formats:
* a2
* A2
* 2a
* 2A
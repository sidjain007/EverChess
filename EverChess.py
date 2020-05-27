class Board:
    def __init__(self, size=8):
        self.size = size
        self.whitePieces = set()
        self.blackPieces = set()
        self.grid = self.newBoard()

    def __str__(self):
        output = "\n"
        footer = "   "
        for i in range(self.size):
            output += str(self.size - i) + " |" + "|".join(self.grid[i]) + "|\n"
            footer += chr(97 + i) + " "

        return output + footer + "\n"

    def newBoard(self):
        grid = []
        for row in range(self.size):
            if row == 1:  # 2nd from top row is black pawns
                add = ['B'] * self.size
                for col in range(self.size):
                    self.blackPieces.add((row, col))
            elif row == self.size - 2:  # 2nd from bottom row is white pawns
                add = ['W'] * self.size
                for col in range(self.size):
                    self.whitePieces.add((row, col))
            else:
                add = [' '] * self.size
            grid.append(add)
        return grid

    def getMoves(self, turn, moved):
        moves = {}
        hasCapture = False

        if turn[0] == 'W':
            direction = -1  # white pawns move 'up'
            pieces = self.whitePieces
            opponent = 'B'
        else:
            direction = 1   # black pawns move 'down'
            pieces = self.blackPieces
            opponent = 'W'

        for piece in pieces:
            if piece in moved:
                continue
            # check straight move
            pos = (piece[0] + direction, piece[1])
            if self.grid[pos[0]][pos[1]] == ' ':  # check if open space
                moves[piece] = {pos: "space"}

            # check diagonal captures
            for pos in [(piece[0] + direction, piece[1] + 1), (piece[0] + direction, piece[1] - 1)]:
                if pos[1] < 0 or pos[1] == self.size:  # checking out of bounds
                    continue
                if self.grid[pos[0]][pos[1]] == opponent:
                    hasCapture = True
                    if piece in moves:
                        moves[piece][pos] = "capture"
                    else:
                        moves[piece] = {pos: "capture"}
        return moves, hasCapture

class Game:
    def __init__(self, boardSize = 8):
        self.gameOver = False
        self.board = Board(boardSize)
        self.turn = 'White'  # white always starts
        self.curPlayer = self.board.whitePieces
        self.moved = set()

    def endGame(self, message):
        """
        Call this function after determining game should end
        """
        print(self.board)
        print("Game over! " + message)
        self.gameOver = True

    def checkReachWin(self, color, row):
        """
        Win by reaching the other side
        """
        if color[0] == 'W' and row == 0:
            self.endGame("White reached the end. White wins!\n")
        elif color[0] == 'B' and row == self.board.size - 1:
            self.endGame("Black reached the end. Black wins!\n")

    def checkNoMoveLoss(self, moves):
        """
        Lose by not having any possible valid moves to make
        """
        if not moves:
            winner = "Black" if self.turn[0] == "W" else "White"
            self.endGame(self.turn + " has nowhere to move. " + winner + " wins!\n")

    def parsePosition(self, parse):
        """
        Checking string input for format [Row#][ColLetter] or [ColLetter][Row#] (and not case sensitive)
        """

        if len(parse) == 2:
            ch1 = ord(parse[0].lower())
            ch2 = ord(parse[1].lower())

            maxNum = 48 + self.board.size  # ascii of max row #

            # [Row#][ColLetter]] case
            if 48 < ch1 <= maxNum and 97 <= ch2 < (97 + self.board.size):
                return maxNum - ch1, ch2 - 97  # actual grid indexes of desired position

            # [ColLetter][Row#] case
            if 48 < ch2 <= maxNum and 97 <= ch1 < (97 + self.board.size):
                return maxNum - ch2, ch1 - 97  # actual grid indexes of desired position
        return False

    def choosePawn(self, moves, hasCapture):
        while True:
            parse = input("Choose pawn to move (ex: a2): ").strip()
            startLoc = self.parsePosition(parse)
            if not startLoc:
                print("Invalid input. Try again")
                continue

            if startLoc not in self.curPlayer:
                print("You don't have a pawn there. Try again")
                continue

            if startLoc not in moves:
                print("This pawn already moved this turn or has no possible moves. Try another pawn")
                continue

            if hasCapture and "capture" not in moves[startLoc].values():
                print("You must make a capture move. Choose a pawn that can capture")
                continue

            return startLoc

    def suggestMoves(self, startLoc, moves, hasCapture):
        """
        Returns a string of the possible moves a pawn can make
        """
        suggest = ""
        for move in moves[startLoc]:
            if hasCapture:
                if moves[startLoc][move] == "capture":
                    suggest += chr(move[1] + 97) + str(self.board.size - move[0]) + " "
            else:
                suggest += chr(move[1] + 97) + str(self.board.size - move[0]) + " "
        return suggest

    def chooseMove(self, startLoc, moves, hasCapture):
        suggest = self.suggestMoves(startLoc, moves, hasCapture)
        while True:
            parse = input("Choose from possible moves [ " + suggest + "] or 'change' to reselect pawn: ").strip()
            if parse == "change" or parse == "'change'":
                startLoc = self.choosePawn(moves, hasCapture)
                suggest = self.suggestMoves(startLoc, moves, hasCapture)
                continue
            moveLoc = self.parsePosition(parse)
            if not moveLoc:
                print("Invalid input. Try again")
                continue

            if moveLoc not in moves[startLoc]:
                print("Can't move there. Try again")
                continue

            if hasCapture and moves[startLoc][moveLoc] != "capture":
                print("You need to make a capture move. Try again")
                continue

            return moveLoc, startLoc

    def gameStep(self):
        print(self.board)
        print(self.turn + "'s turn\n")
        moves, hasCapture = self.board.getMoves(self.turn, self.moved)
        self.checkNoMoveLoss(moves)
        if self.gameOver:
            return

        startLoc = self.choosePawn(moves, hasCapture)
        moveLoc, startLoc = self.chooseMove(startLoc, moves, hasCapture)

        # update player's pieces
        self.curPlayer.add(moveLoc)
        self.curPlayer.remove(startLoc)

        # update the actual game board
        self.board.grid[startLoc[0]][startLoc[1]] = ' '
        self.board.grid[moveLoc[0]][moveLoc[1]] = self.turn[0]

        # on captures, mark pawn as piece that can't move again this turn and remove opponent piece
        if hasCapture:
            self.moved.add(moveLoc)
            otherPlayer = self.board.blackPieces if self.turn[0] == 'W' else self.board.whitePieces
            otherPlayer.remove(moveLoc)

        self.checkReachWin(self.turn, moveLoc[0])
        if self.gameOver:
            return

        # end of current player's turn if no capture
        if not hasCapture:
            self.moved = set()  # reset pawns moved on this turn
            if self.turn[0] == 'W':
                self.turn = 'Black'
                self.curPlayer = self.board.blackPieces
            else:
                self.turn = 'White'
                self.curPlayer = self.board.whitePieces


def driver():
    print("\nWelcome to EverChess!\n")
    while True:
        if input("Press enter to play or any other key to quit: ") != "":
            break
        game = Game()
        while not game.gameOver:
            game.gameStep()
    print("Thanks for playing!")


if __name__ == "__main__":
    driver()

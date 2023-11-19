class Boardclass:
    """A class to create a gameboard object that stores game information.

    Creates a gameboard object that stores the moves and stats of each player.
    """

    def __init__(self, current_player: str = "", last_player: str = "", player_symbol: str = "", other_symbol: str = "",
                 num_games: int = 0, num_wins: int = 0, num_losses: int = 0, num_ties: int = 0) -> None:
        """A function to initialize variables for Boardclass to store data used during the game.

        Creates variables that represent the gameboard, the current player, the player that last moved, the player's
        symbol, the other player's symbol, the number of games, the number of wins, the number of losses, and the
        number of ties.
        """

        self.gameboard = []
        self.current_player = current_player
        self.last_player = last_player
        self.symbol = player_symbol
        self.other_symbol = other_symbol
        self.num_games = num_games
        self.num_wins = num_wins
        self.num_losses = num_losses
        self.num_ties = num_ties

    def updateGamesPlayed(self) -> None:
        """A function to update the number of games played.

        Increments the number of games played by 1 whenever called.
        """
        self.num_games += 1

    def resetGameBoard(self) -> list:
        """A function to reset the gameboard to start a new game.

        Redefines the values of the spaces to empty strings and prints the board so that all the spaces are cleared of
        moves and symbols.

        Returns:
            self.gameboard: a list of lists, representing the 3 rows, filled with empty strings to represent the nine
            spaces in a tic-tac-toe board.
        """
        line = "-----------------"
        self.gameboard = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        print(f"  {self.gameboard[0][0]}  |  {self.gameboard[0][1]}  |  {self.gameboard[0][1]}")
        print(line)
        print(f"  {self.gameboard[1][0]}  |  {self.gameboard[1][1]}  |  {self.gameboard[1][1]}")
        print(line)
        print(f"  {self.gameboard[2][0]}  |  {self.gameboard[2][1]}  |  {self.gameboard[2][1]}")
        print()

        return self.gameboard

    def updateGameBoard(self, move: str, symbol: str) -> list:
        """A function to update the game board every time a move is made.

        Based on the value inputted into the move variable, assigns the first number as the row and the second number
        as the column. Adds the player's symbol into the designated space and then prints the gameboard with the updated
        move.

        Args:
            move: a string of 2 numbers that represent the row and column of the move being made
            symbol: the string 'X' or 'O', representing the symbol of the player making the move

        Returns:
            self.gameboard: a list of lists, representing the 3 rows, filled with strings to represent the nine
            spaces in a tic-tac-toe board, with the move just made added
        """
        line = "-----------------"

        row = int(move[0])
        column = int(move[1])

        self.gameboard[row][column] = symbol

        print(f"  {self.gameboard[0][0]}  |  {self.gameboard[0][1]}  |  {self.gameboard[0][2]}")
        print(line)
        print(f"  {self.gameboard[1][0]}  |  {self.gameboard[1][1]}  |  {self.gameboard[1][2]}")
        print(line)
        print(f"  {self.gameboard[2][0]}  |  {self.gameboard[2][1]}  |  {self.gameboard[2][2]}")
        print()

        return self.gameboard

    def checkMove(self, row: int, column: int) -> bool:
        """A function to check if a move being played already exists on the board.

        Based on the values of the row and column of the move being made, if space the player wants to move is
        empty, returns True. If the space is already taken, returns False.

        Args:
            row: the integer representing the row on the board where the player wants to move
            column: the integer representing the column on the board where the player wants to move

        Returns:
            boolean: If the space is empty, returns true. If the space is taken, returns False.
        """

        if self.gameboard[row][column] == " ":
            return True
        else:
            return False

    def decodeMove(self, move: int) -> str:
        """A function to change the move into a string of numbers for the row and column.

        For each possible move, returns the string of the designated row and column that move exists on the board to
        change the value of the space from empty to a symbol.

        Returns:
            a string containing the number of the row and the number of the column of the space.
        """
        if move == 1:
            return "00"
        if move == 2:
            return "01"
        if move == 3:
            return "02"
        if move == 4:
            return "10"
        if move == 5:
            return "11"
        if move == 6:
            return "12"
        if move == 7:
            return "20"
        if move == 8:
            return "21"
        if move == 9:
            return "22"

    def isWinner(self, symbol: str) -> bool:
        """A function to detect when a move results in a win.

        Checks if the symbol exists in a winning pattern.

        Args:
            symbol: the symbol of the player making the move.

        Returns:
            True if the designated symbol in the argument exists across an entire row.
        """
        if (symbol in self.gameboard[0][0]) and (symbol in self.gameboard[0][1]) and (symbol in self.gameboard[0][2]):
            return True

        elif (symbol in self.gameboard[1][0]) and (symbol in self.gameboard[1][1]) and (symbol in self.gameboard[1][2]):
            return True

        elif (symbol in self.gameboard[2][0]) and (symbol in self.gameboard[2][1]) and (symbol in self.gameboard[2][2]):
            return True

        elif (symbol in self.gameboard[0][0]) and (symbol in self.gameboard[1][0]) and (symbol in self.gameboard[2][0]):
            return True

        elif (symbol in self.gameboard[0][1]) and (symbol in self.gameboard[1][1]) and (symbol in self.gameboard[2][1]):
            return True

        elif (symbol in self.gameboard[0][2]) and (symbol in self.gameboard[1][2]) and (symbol in self.gameboard[2][2]):
            return True

        elif (symbol in self.gameboard[0][0]) and (symbol in self.gameboard[1][1]) and (symbol in self.gameboard[2][2]):
            return True

        elif (symbol in self.gameboard[0][2]) and (symbol in self.gameboard[1][1]) and (symbol in self.gameboard[2][0]):
            return True

    def boardIsFull(self) -> bool:
        """
        A function to check whether all the spaces are filled in a board and increments the tie count.

        Returns:
             True if all the spaces are taken, False if not.
        """
        if (" " not in self.gameboard[0]) and (" " not in self.gameboard[1]) and (" " not in self.gameboard[2]):
            self.num_ties += 1
            return True
        else:
            return False

    def printStats(self) -> None:
        """A function to print the stats at the end of a game.

        Prints the current player, last player, number of games played, number of wins, number of losses, and number
        of ties.
        """
        print("Stats:")
        print("Current Player:", self.current_player)
        print("Last player to make a move:", self.last_player)
        print("Number of Games Played:", self.num_games)
        print("Number of Wins:", self.num_wins)
        print("Number of Losses:", self.num_losses)
        print("Number of Ties:", self.num_ties)


class BoardClass:
    """A class to store and handle information for the game board and player stats
        Attributes:
            current_player (str): the username of the player
            last_player (str): the username of the last player
            num_wins (int): the number of winning games
            num_ties (int): the number of tied games
            num_losses (int): the number of lost games
            num_games_played(int): the total number of games played
    """
    gameBoard = 0

    def __init__(self, current_player: str = '', last_player: str = '', num_wins: int = 0, num_ties: int = 0,
                 num_losses: int = 0, num_games_played: int = 0) -> None:
        """Creates a game board.

        Initializes relevant variables using args such as current_player, last_player, num_wins, num_ties, num_looses,
        and num_games_played
        """
        self.current_player = current_player
        self.last_player = last_player
        self.num_wins = num_wins
        self.num_ties = num_ties
        self.num_losses = num_losses
        self.num_games_played = num_games_played

    def startGame(self) -> list:
        """Starts a game of Tic Tac Toe.

        Updates the number of games played by adding 1 to the variable count, creates a blank board to start the game
        using resetGameBoard(), and draws the game board using drawGameBoard(). Returns the board as a list.
        """
        print("\nStarting Game.")
        self.updateGamesPlayed()
        board = self.resetGameBoard()
        self.drawGameBoard(board)
        return board

    def updateGamesPlayed(self) -> None:
        """Updates the total number of games played.

        Increments the num_games_played counter by adding one to value of the variable.
        """
        self.num_games_played += 1

    def currentPlayer(self, current_player) -> str:
        """Updates the value of the current player variable in the class.

        Uses the argument current_player to update self.current_player to accurately represent the name of the
        current player each time it is called.
        """
        self.current_player = current_player
        return self.current_player

    def lastPlayer(self, last_player) -> str:
        """Updates the value of last player variable in the class.

        Uses the argument last_player to update the value of self.last_player to accurately represent the name of the
        last player each time it is called."""
        self.last_player = last_player
        return self.last_player

    def drawGameBoard(self, board) -> None:
        """Draws a visual representation of the game board.

        Uses the argument board to input the values of the board stored in the list and draws the game board out using
        a more appealing visual representation to display every turn.
        """
        row1 = [f'  {board[0][0]}  |  {board[0][1]}  |  {board[0][2]}  ']
        divider1 = ["------------------"]
        row2 = [f'  {board[1][0]}  |  {board[1][1]}  |  {board[1][2]}  ']
        divider2 = ["------------------"]
        row3 = [f'  {board[2][0]}  |  {board[2][1]}  |  {board[2][2]}  ']

        visualBoard = [row1, divider1, row2, divider2, row3]

        for row_or_divider in visualBoard:
            for element in row_or_divider:
                print(element)
        print()

    def resetGameBoard(self) -> list:
        """Resets the game board and clears all spaces.

        Sets the values of all the spaces to blank and applies it to the board list. Returns board as a list to be used
        for each game.
        """
        space1 = " "
        space2 = " "
        space3 = " "
        space4 = " "
        space5 = " "
        space6 = " "
        space7 = " "
        space8 = " "
        space9 = " "

        row1 = [space1, space2, space3]
        row2 = [space4, space5, space6]
        row3 = [space7, space8, space9]
        board = [row1, row2, row3]
        return board

    def updateGameBoard(self, board, player_move, playerSymbol) -> list:
        """Updates the game board by adding the player move to the designated space on the board.

        Uses the value of player_move to find the corresponding column and row to put the player's symbol in the correct
        space on the board. Returns the updated board.
        """
        column = int(player_move[0])
        row = int(player_move[1])
        board[(row - 1)][(column - 1)] = playerSymbol
        return board

    def isWinner(self, board, symbol, loseCondition) -> bool:
        """Checks whether the move just made was a winning move.

        Checks every possible winning formation on the board to see if any apply to the current board. Updates the
        number of wins if the board is a winning board, or updates the number of losses if the player lost. Uses a
        boolean win condition variable to check if any of the if statements were fulfilled, and returns either True or
        False.
        """
        winCondition = False

        if loseCondition is True:
            self.num_losses += 1

        if (symbol in board[0][0]) and (symbol in board[0][1]) and (symbol in board[0][2]):
            winCondition = self.updateWins()

        elif (symbol in board[1][0]) and (symbol in board[1][1]) and (symbol in board[1][2]):
            winCondition = self.updateWins()

        elif (symbol in board[2][0]) and (symbol in board[2][1]) and (symbol in board[2][2]):
            winCondition = self.updateWins()

        elif (symbol in board[0][0]) and (symbol in board[1][0]) and (symbol in board[2][0]):
            winCondition = self.updateWins()

        elif (symbol in board[0][1]) and (symbol in board[1][1]) and (symbol in board[2][1]):
            winCondition = self.updateWins()

        elif (symbol in board[0][2]) and (symbol in board[1][2]) and (symbol in board[2][2]):
            winCondition = self.updateWins()

        elif (symbol in board[0][0]) and (symbol in board[1][1]) and (symbol in board[2][2]):
            winCondition = self.updateWins()

        elif (symbol in board[0][2]) and (symbol in board[1][1]) and (symbol in board[2][0]):
            winCondition = self.updateWins()

        return winCondition

    def updateWins(self) -> bool:
        """Updates the number of winning games.

        Increments the number of wins by adding one to the current value of num_wins. Returns True to update the win
        condition variable in isWinner().
        """
        self.num_wins += 1
        return True

    def boardIsFull(self, board) -> bool:
        """Checks the spaces on the game board to see if the current board is a tied game.

        Checks each space in every row to see if there are any blank spaces. If there are no blank spaces, then there
        are no more moves to be made, and the game is tied. Returns True or False depending on whether the board is
        full or not. If it is a tied game, the number of tied games is incremented.
        """
        if (" " not in board[0]) and (" " not in board[1]) and (" " not in board[2]):
            print("Tied Game")
            self.num_ties += 1
            return True
        else:
            return False

    def printStats(self) -> None:
        """Prints out the stats after the game is over.

        Uses the variables current_player, last_player, num_games_played, num_wins, num_losses, and num_ties to display
        their values in a list of stats unique to each user.
        """
        print("Stats:")
        print("Current Player:", self.current_player)
        print("Last player to make a move:", self.last_player)
        print("Number of Games Played:", self.num_games_played)
        print("Number of Wins:", self.num_wins)
        print("Number of Losses:", self.num_losses)
        print("Number of Ties:", self.num_ties)

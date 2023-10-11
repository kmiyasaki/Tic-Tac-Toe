from gameboard import BoardClass
import socket


class Player1Socket:
    """A class to create a socket for player one and store information about Player 1's game.

    Creates a game board for player 1 and initializes variables relating to player 1's information, such as p1username
    and playerSymbol to easily store and refer to throughout the game. Runs functions tryConnection(),
    usernameExchange(), createBoard(), and runGame() to create a connection between player 1 and player 2's sockets
    and to get the game started.
    """
    player1socket = 0

    def __init__(self) -> None:
        """Creates a game board, a socket, and initializes Player 1's variables.

        Initializes p1username, playerSymbol, otherPlayerSymbol, and p2username to use during the game, and runs the
        functions tryConnection() to create a connection between player 1 and player 2, usernameExchange() to allow
        players to exchange usernames, createBoard() to create a game board, and runGame() to start the game.
        """
        self.p1gameBoard = None
        self.p1username = ''
        self.playerSymbol = 'X'
        self.otherPlayerSymbol = 'O'
        self.player1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2username = ''

        self.tryConnection()
        self.usernameExchange()
        self.createBoard()
        self.runGame()

    def createBoard(self) -> None:
        """Creates a game board for player 1.

        Uses BoardClass to create player 1's game board, and specifies that the current player is player 1.
        """
        self.p1gameBoard = BoardClass(current_player=self.p1username)

    def tryConnection(self) -> None:
        """Tries to establish a connection between player 1 and player 2 using the given host and port information.

        Uses a try/except and the function createConnection() to try to establish a connection. If unsuccessful, calls
        the function connectionLoop() to prompt for the host and port information again. Uses the boolean variable
        connect to specify whether a connection has been made or not.
        """
        connect = False
        while connect is False:
            try:
                self.createConnection()
                print("\nConnection Successful!\n")
            except:
                self.connectionLoop()
            connect = True

    def promptConnectionInfo(self) -> tuple:
        """Prompts the user for the host and port information.

        Uses built-in input function to ask the user for the host and port information to try to create a connection.
        Returns the host and port information as a tuple.
        """
        player2host = input("What is the host name/IP address of player 2?\n")
        port = int(input("What port to use?\n"))
        return player2host, port

    def createConnection(self) -> None:
        """Creates a connection using the given host and port information.

        Uses player 1's socket to try to create a connection by calling promptConnectionInfo() to ask for the host and
        port information, and uses it to try to connect.
        """
        host, port = self.promptConnectionInfo()
        self.player1socket.connect((host, port))

    def tryAgainPrompt(self) -> str:
        """Prompts the user if they want to try again after a connection was failed to be established.

        Asks the user for a yes or no answer for whether they want to try to create a connection after it was failed
        to be established, and returns their answer in a string.
        """
        tryAgainAnswer = input("Connection cannot be made. Want to try again? (y/n)\n")
        return tryAgainAnswer

    def connectionLoop(self) -> None:
        """Error checks the user's answer after tryAgainPrompt() is called.

        If the user said yes, a tryConnection() is called again, if the user said no, the program is quit, and if the
        user did not input a valid answer, then they are prompted again until a valid answer is inputted.
        """
        loopContinue = True
        programQuit = False

        while loopContinue is True:
            user_answer = self.tryAgainPrompt()

            if (user_answer[0] == 'y') or (user_answer[0] == 'Y'):
                loopContinue = False
            elif (user_answer[0] == 'n') or (user_answer[0] == 'N'):
                programQuit = True
                loopContinue = False
            else:
                print("Error: Please enter either 'y' or 'n'.")
                continue

        if programQuit is True:
            quit()
        if loopContinue is False:
            self.tryConnection()

    def sendData(self, data) -> None:
        """Uses player 1's socket to send data to player 2.

        Allows information to easily be sent to player 2 using player 1's socket. The argument data is a string of what
        will be sent.
        """
        self.player1socket.sendall(data.encode())

    def receiveData(self) -> str:
        """Uses player 1's socket to receive data from player 2.

        Allows information to easily be received from player 2. The data sent over is returned as a string.
        """
        receivedData = self.player1socket.recv(1024).decode()
        return receivedData

    def usernameExchange(self) -> None:
        """Allows users to exchange usernames after a connection is made.

        Prompts player 1 to input a valid username to send to player 2. If the username is not alphanumeric, they are
        prompted until a valid answer is inputted. Once a valid username is inputted, the usernames are transmitted
        to each player.
        """
        valid = False
        while valid is False:
            self.p1username = input("Please enter an alphanumeric username to send to player2:\n")
            if self.p1username.isalnum():
                valid = True
            if valid is False:
                print("Invalid username. Please try again.")

        self.sendData(self.p1username)
        self.p2username = self.receiveData()
        print(f"\nPlayer 1's username: {self.p1username}")
        print(f"Player 2's username: {self.p2username}")

    def playerMove(self, board) -> str:
        """Prompts the user which space they want to make a move on using an inputted value for the corresponding row
        and column on the board.

        User is asked which column and row they want to play, and if the move is in the domain of the board and if the
        space is not already taken, the move is returned as a string containing the row and column number.
        """
        inDomain = False
        validMove = False
        while (validMove is False) or (inDomain is False):
            playerMoveX = input("What is the column of the space you want to move? (1, 2, 3, Left to Right)\n")
            playerMoveY = input("What is the row of the space you want to move? (1, 2, 3, Top to Bottom)\n")
            if (playerMoveX in ('1', '2', '3')) and (playerMoveY in ('1', '2', '3')):
                inDomain = True
            else:
                print("\nInvalid move. Please choose a column and row 1-3.")
                continue

            if board[int(playerMoveY) - 1][int(playerMoveX) - 1] == ' ':
                validMove = True
            else:
                print("\nInvalid move. Space is already filled.")
                continue

        playerMove = ""
        playerMove += playerMoveX
        playerMove += playerMoveY
        print(f"{self.p1username}'s Move: Column {playerMoveX}, Row {playerMoveY}\n")
        return playerMove

    def p1gameOver(self) -> None:
        """Prompts the user if they wish to play another game once a game has ended.

        Calls printStats() once a game has ended, and prompts the user until a valid answer has been inputted if they
        want to play another game. If they want to play another game, another game is started. If they do not, the
        program is ended.
        """
        self.p1gameBoard.printStats()

        againPrompt = True
        programQuit = False
        while againPrompt is True:
            playAgain = input("\nDo you wish to play again? (y/n)\n")

            if (playAgain[0] == "y") or (playAgain[0] == "Y"):

                againPrompt = False
                self.sendData(playAgain)
                self.sendData("\nPlay Again")
            elif (playAgain[0] == "n") or (playAgain[0] == "N"):
                againPrompt = False
                programQuit = True
                self.sendData(playAgain)
                self.sendData("\nFun Times")
            else:
                print("Error: Please enter either 'y' or 'n'.")
                continue

        if programQuit is True:
            quit()
        if againPrompt is False:
            self.runGame()

    def p1receiveMove(self) -> str:
        """Waits until player 1 receives player 2's move.

        Calls receiveData() to receive player 2's moves, and returns the received data as a string of the row and
        column where player 2 moved.
        """
        print(f"Waiting for {self.p2username} to make a move...\n")
        p2move = self.receiveData()
        print(f"{self.p2username}'s Move: Column {p2move[0]}, Row {p2move[1]}\n")
        return p2move

    def runGame(self) -> None:
        """Starts and uses an infinite loop to run a game of Tic Tac Toe until the game is won or tied.

        Uses an infinite while loop to keep asking player 1 for their move and to keep receiving player 2's move. Each
        time a move is made, the board is updated, drawn, and checked in case the last move made was a winning move.
        The board is also checked for ties after every move. Uses functions sendData() and receiveData() to transmit
        data between player 1 and player 2.
        """
        player1gameBoard = self.p1gameBoard.startGame()
        self.p1gameBoard.currentPlayer(self.p1username)

        while True:
            p1move = self.playerMove(player1gameBoard)
            move = self.p1gameBoard.updateGameBoard(player1gameBoard, p1move, self.playerSymbol)
            self.p1gameBoard.drawGameBoard(move)

            if self.p1gameBoard.isWinner(player1gameBoard, self.playerSymbol, False) is True:
                self.p1gameBoard.lastPlayer(self.p1username)
                print('You Win!\n')
                self.sendData(p1move + "LOST GAME")
                self.p1gameOver()
            else:
                self.sendData(p1move)

            if self.p1gameBoard.boardIsFull(player1gameBoard) is True:
                self.p1gameBoard.lastPlayer(self.p1username)
                self.p1gameOver()

            p2move = self.p1receiveMove()
            move = self.p1gameBoard.updateGameBoard(player1gameBoard, p2move[:2], self.otherPlayerSymbol)
            self.p1gameBoard.drawGameBoard(move)

            if len(p2move) != 2:
                self.p1gameBoard.isWinner(player1gameBoard, self.playerSymbol, True)
                self.p1gameBoard.lastPlayer(self.p2username)
                print("You Lose!\n")
                self.p1gameOver()

            if self.p1gameBoard.boardIsFull(player1gameBoard) is True:
                self.p1gameBoard.lastPlayer(self.p2username)
                self.p1gameOver()


if __name__ == "__main__":
    Player1Socket()

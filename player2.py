from gameboard import BoardClass
import socket


class Player2Socket:
    """A class to create a socket for player one and store information about Player 2's game.

    Creates a game board for player 2 and initializes variables relating to player 2's information, such as p2username
    and playerSymbol to easily store and refer to throughout the game. Runs functions tryConnection(),
    usernameExchange(), createBoard(), and runGame() to create a connection between player 1 and player 2's sockets
    and to get the game started.
    """
    player2socket = 0

    def __init__(self) -> None:
        """Creates a game board, a socket, and initializes Player 2's variables.

        Initializes p1username, playerSymbol, otherPlayerSymbol, and p2username to use during the game, and runs the
        functions acceptConnection() to create a connection between player 1 and player 2, usernameExchange() to allow
        players to exchange usernames, createBoard() to create a game board, and runGame() to start the game.
        """

        self.p2gameBoard = None
        self.p2username = 'player2'
        self.p1username = ''
        self.playerSymbol = 'O'
        self.otherPlayerSymbol = 'X'
        self.player2socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2address = ''
        self.p2port = 0
        self.clientSocket = ''
        self.clientAddress = ''

        self.hostInfoPrompt()
        self.bindSocket(self.p2address, self.p2port)
        self.acceptConnection()
        self.usernameExchange()
        self.createBoard()
        self.runGame()

    def hostInfoPrompt(self) -> None:
        """Prompts user for the host and port information.

        Uses built-in input function to ask the user for the host and port information to be used to bind the socket.
        """
        self.p2address = input("Please provide your host name/IP address.\n")
        self.p2port = int(input("Please provide your port number.\n"))

    def createBoard(self) -> None:
        """Creates a game board for player 2.

        Uses BoardClass to create player 2's game board, and specifies that the current player is player 2.
        """
        self.p2gameBoard = BoardClass(current_player=self.p2username)

    def bindSocket(self, address, port) -> None:
        """Binds a socket using host and port information.

        After a socket is bound using the given information address and port in the arguments, waits for player 1 to
        connect.
        """
        self.player2socket.bind((address, port))
        self.player2socket.listen(1)
        print("Waiting for player 1 to connect...\n")

    def acceptConnection(self) -> None:
        """Accepts incoming connections from player 1.

        After player 1 inputs valid host and port information, accepts the information to create a connection between
        player 1 and player 2.
        """
        self.clientSocket, self.clientAddress = self.player2socket.accept()
        print(f"Client connected from: {self.clientAddress}\n")

    def receiveData(self) -> str:
        """Uses player 2's socket to receive data from player 1.

        Allows information to easily be received from player 1. The data sent over is returned as a string.
        """
        receivedData = self.clientSocket.recv(1024).decode()
        return receivedData

    def sendData(self, data) -> None:
        """Uses player 2's socket to send data to player 1.

        Allows information to easily be sent to player 1 using player 2's socket. The argument data is a string of what
        will be sent.
        """
        self.clientSocket.sendall(data.encode())

    def usernameExchange(self) -> None:
        """Allows users to exchange usernames after a connection is made.

        Receives player 1's username and sends player 2's username. Once both usernames have been communicated,
        displays both usernames.
        """
        self.p1username = self.receiveData()
        print(f"Player 1's username: {self.p1username}")
        print("Player 2's username: player2")
        self.sendData(self.p2username)

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

        print(f'{self.p2username} Move: Column {playerMoveX}, Row {playerMoveY}\n')

        return playerMove

    def p2receiveMove(self) -> str:
        """Waits until player 2 receives player 1's move.

        Calls receiveData() to receive player 1's moves, and returns the received data as a string of the row and
        column where player 1 moved.
        """
        print(f"Waiting for {self.p1username} to make a move...\n")
        p1move = self.receiveData()
        print(f"{self.p1username} Move: Column {p1move[0]}, Row {p1move[1]}\n")
        return p1move

    def p2gameOver(self):
        """Prompts the user if they wish to play another game once a game has ended.

        Calls printStats() once a game has ended, and prompts the user until a valid answer has been inputted if they
        want to play another game. If they want to play another game, another game is started. If they do not, the
        program is ended.
        """
        self.p2gameBoard.printStats()
        playAgain = self.receiveData()

        if (playAgain[0] == "y") or (playAgain[0] == "Y"):
            print(self.receiveData())
            self.runGame()
        elif (playAgain[0] == "n") or (playAgain[0] == "N"):
            print(self.receiveData())
            quit()

    def runGame(self) -> None:
        """Starts and uses an infinite loop to run a game of Tic Tac Toe until the game is won or tied.

        Uses an infinite while loop to keep asking player 2 for their move and to keep receiving player 1's move. Each
        time a move is made, the board is updated, drawn, and checked in case the last move made was a winning move.
        The board is also checked for ties after every move. Uses functions sendData() and receiveData() to transmit
        data between player 1 and player 2.
        """
        player2gameBoard = self.p2gameBoard.startGame()
        self.p2gameBoard.currentPlayer(self.p2username)

        while True:
            p1move = self.p2receiveMove()
            move = self.p2gameBoard.updateGameBoard(player2gameBoard, p1move[:2], self.otherPlayerSymbol)
            self.p2gameBoard.drawGameBoard(move)

            if len(p1move) != 2:
                self.p2gameBoard.isWinner(player2gameBoard, self.playerSymbol, True)
                self.p2gameBoard.lastPlayer(self.p1username)
                print("You Lose!\n")
                self.p2gameOver()

            if self.p2gameBoard.boardIsFull(player2gameBoard) is True:
                self.p2gameBoard.lastPlayer(self.p1username)
                self.p2gameOver()

            p2move = self.playerMove(player2gameBoard)
            move = self.p2gameBoard.updateGameBoard(player2gameBoard, p2move, self.playerSymbol)
            self.p2gameBoard.drawGameBoard(move)
            
            if self.p2gameBoard.isWinner(player2gameBoard, self.playerSymbol, False) is True:
                self.p2gameBoard.lastPlayer(self.p2username)
                print('You Win!\n')
                self.sendData(p2move + 'LOST GAME')
                self.p2gameOver()
            else:
                self.sendData(p2move)

            if self.p2gameBoard.boardIsFull(player2gameBoard) is True:
                self.p2gameBoard.lastPlayer(self.p2username)
                self.p2gameOver()


if __name__ == "__main__":
    Player2Socket()

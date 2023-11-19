import socket
from gameboard import Boardclass


class Player2:
    """A class to create a Player 2 object that stores player and game information.

    Creates a player object and an object that stores player 2's gameboard. Initializes player 2's username, symbol,
    and socket and prompts the user for player 2's host information to create a socket connection between the two
    players. Uses sockets to send and receive moves from player 1, and uses the gameboard object to store each move.
    All inputs are checked for validity, and the board checks for wins and ties after each move. Statistics are stored
    to print at the end of the game session.
    """

    def __init__(self) -> None:
        """Initializes player variables to store and use data throughout the game.

        Sets initial values for the player usernames, player 2's socket, and symbols of both players to store and use
        the variables during the game.
        """
        self.p2username = ""
        self.p1username = ""
        self.p2socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2symbol = "O"
        self.p1symbol = "X"

    def askForHostInfo(self) -> tuple:
        """Prompts user for host information of player 2.

        Asks the user for the ip address and port of player 2 to use to create a socket connection between both players.

        Returns:
            A tuple containing the IP address and port number of player 2 from user input.
        """
        ip_address = input("Please input your host name/IP address.\n")
        port = int(input("Please input your port number.\n"))

        return ip_address, port

    def attemptConnection(self) -> None:
        """A function to attempt to connect to player 1's socket.

        Uses bind and listen functions to connect to player 1. After successful connection, calls sendUsername().
        """
        self.p2socket.bind(self.askForHostInfo())
        self.p2socket.listen(1)

        self.clientSocket, self.clientAddress = self.p2socket.accept()
        print('Connection Successful!\n')
        self.sendUsername()

    def sendUsername(self) -> None:
        """A function to exchange usernames between players 1 and 2.

        The username of player 1 is received. Both usernames are then displayed on the screen.
        """
        print("Waiting for Player 1 to send their username...")
        self.p1username = self.receiveData()
        print("\nPlayer 1:", self.p1username)
        print("Player 2: player2")
        print()

        self.p2username = 'player2'
        self.sendData(self.p2username)

    def sendData(self, data: str) -> None:
        """A function to send data strings to player 2.

        Uses player 1's socket to encode and send data to player 2.

        Args:
            data: a string to send to player 2.
        """
        self.clientSocket.sendall(data.encode())

    def receiveData(self) -> str:
        """A function to receive data from player 1.

        Uses player 2's socket to receive and decode data strings from player 2.

        Returns:
            a string containing data sent from player 1.
        """
        return self.clientSocket.recv(1024).decode()

    def playerMove(self) -> tuple:
        """A function to prompt the user to make a move and send it to player 2.

        The user is prompted to enter a number 1-9 to indicate the space they would like to move. The function
        checkMove() is then called for the user to input their move, and is then translated to the move's corresponding
        row and column. The row and column string values are then sent to player 2.

        Returns:
            (row, column): a tuple containing the corresponding row and column of the move inputted by the user.
        """
        print("Enter the number of the space you would like to move.")
        print("1 | 2 | 3")
        print("4 | 5 | 6")
        print("7 | 8 | 9")

        row, column = self.checkMove()
        self.sendData(f"{row}{column}")

        return row, column

    def checkMove(self) -> tuple:
        """A function to prompt player 2 to enter their move and checks the input for validity.

        Loops until a valid input and move is inputted by player 1. Prompts the user to enter their move, and if the
        value is a number 1-9 and if the space has not already been taken, then the corresponding row and column of the
        move is returned as a tuple. The user is re-prompted to enter their move if they input an invalid move.

        Returns:
            (row, column): a tuple containing the corresponding row and column of the move inputted by the user.
        """
        # Check if player move is a valid value
        valid_input = False
        valid_move = False

        while (valid_input and valid_move) is False:
            move = input("Your Move: ")

            # checks if move is valid value
            if move in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                valid_input = True

            # if move is valid, is the space empty
            if valid_input is True:
                decoded_move = p2board.decodeMove(int(move))
                row = int(decoded_move[0])
                column = int(decoded_move[1])

                # checks if space has not already been taken
                if p2board.gameboard[row][column] == " ":
                    valid_move = True
                else:
                    print("Invalid input, try again.\n")
                    valid_input = False

            else:
                print("Invalid input, try again.\n")

        return row, column

    def receiveMove(self) -> str:
        """A function to receive a move from player 1.

        Calls the receiveData() function to receive the move player 2 made, and prints it.

        Returns:
            move: the space player 1 inputted that designates where they chose to move.
        """
        print("\nWaiting for Player 1 to move...")
        move = self.receiveData()

        if p2board.boardIsFull() is True:
            p2board.num_ties += 1
        if p2board.isWinner(self.p1symbol) is True:
            p2board.num_losses += 1
            print("loss")

        print()
        print("Player 1's move:")
        return move

    def startGame(self) -> None:
        """A function to start a game between player 1 and 2.

        Indicates that a game has started by printing 'Game Start' and calls the resetGameBoard() function to clear
        the board of all moves and calls updateGamesPlayed() to increment the number of games played for the stats.
        """
        print("Game Start")
        p2board.resetGameBoard()
        p2board.updateGamesPlayed()

    def endGame(self, outcome: str) -> None:
        """A function to end the game once an outcome has been found.

        Based on the outcome of the game designated by the argument, prints the result, and increments the number of
        wins or losses for player 2. Calls playAgain() function to prompt player 1 if they would like to play again. If
        the program has not quit after playAgain() is called, then a new game is started by calling startGame().

        Args:
            outcome: a string that dictates the result of the game, which is either a tie, a win, or a loss for
            player 2.
        """
        if outcome == "tie":
            print("Tied Game\n")
        elif outcome == "win":
            print("You Win!\n")
            p2board.num_wins += 1
        elif outcome == "loss":
            print("You Lose")
            p2board.num_losses += 1

        print("Waiting for Player 1...\n")
        play_again = self.receiveData()
        print(play_again)
        if play_again == "Fun Times":
            p2board.printStats()
            quit()
        elif play_again == "Play Again":
            self.startGame()

    def checkBoard(self, symbol: str) -> bool:
        """A function to check if the board for a winning pattern or to check if the board is full.

        Calls isWinner() for each player to see if either player has won, and calls boardIsFull() to check for ties. In
        all winning or tie outcomes, calls endGame() with corresponding outcome if a win or tie is detected.

        Returns:
            True if a win or a tie is detected.
        """
        if p2board.boardIsFull() is True:
            player2.endGame("tie")
            return True

        if p2board.isWinner(symbol) is True:
            if symbol == player2.p2symbol:
                player2.endGame("win")
                return True
            if symbol == player2.p1symbol:
                player2.endGame("loss")
                return True

        return False

    def runGame(self) -> None:
        """A function to run the game of tic-tac-toe.

        Contains a while loop that continues to prompt player 1 and player 2 to take their turn. Continues for as long
        as the game lasts.
        """
        while True:
            restart_loop = False
            # Player 1 turn
            player1_move = self.receiveMove()
            # update last player
            p2board.last_player = self.p1username
            # update game board
            p2board.updateGameBoard(player1_move, self.p1symbol)
            # check board for wins or ties
            if self.checkBoard(self.p1symbol) is True:
                restart_loop = True

            if restart_loop is False:
                # Player 2 turn
                player2_move = self.playerMove()
                # update last player
                p2board.last_player = self.p2username
                # update game board
                p2board.updateGameBoard(player2_move, self.p2symbol)
                # check board for wins or ties
                self.checkBoard(self.p2symbol)

if __name__ == '__main__':
    player2 = Player2()
    player2.attemptConnection()

    p2board = Boardclass(current_player=player2.p2username, player_symbol=player2.p2symbol,
                         other_symbol=player2.p1symbol)

    player2.startGame()
    player2.runGame()

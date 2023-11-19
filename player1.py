import socket
from gameboard import Boardclass


class Player1:
    """A class to create a Player 1 object that stores player and game information.

    Creates a player object and an object that stores player 1's gameboard. Initializes player 1's username, symbol,
    and socket and prompts the user for player 2's host information to create a socket connection between the two
    players. Uses sockets to send and receive moves from player 2, and uses the gameboard object to store each move.
    All inputs are checked for validity, and the board checks for wins and ties after each move. Statistics are stored
    to print at the end of the game session.
    """

    def __init__(self) -> None:
        """Initializes player variables to store and use data throughout the game.

        Sets initial values for the player usernames, player 1's socket, and symbols of both players to store and use
        the variables during the game.
        """
        self.p1username = ""
        self.p2username = ""
        self.p1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p1symbol = "X"
        self.p2symbol = "O"

    def askForHostInfo(self) -> tuple:
        """Prompts user for host information of player 2.

        Asks the user for the ip address and port of player 2 to use to create a socket connection between both players.

        Returns:
            A tuple containing the IP address and port number of player 2 from user input.
        """
        ip_address = input("What is the host name/IP Address of player 2?\n")
        port = int(input("What port to use?\n"))

        return ip_address, port

    def connect(self) -> None:
        """Attempts to connect player 1's socket using player 2's host information.

        Calls askForHostInfo() and uses returned values of ip address and port to create a connection using player 1's
        socket. Prints success when connected, or raises an error when a connection cannot be made.

        Raises:
            ConnectionRefusedError: an error that occurs when a connection cannot be made with given host information.
        """
        self.p1socket.connect(self.askForHostInfo())
        print('Connection Successful!\n')

    def attemptConnection(self) -> None:
        """A function that uses a while loop until a successful connection is made between player 1 and 2.

        Until a connection is made by calling connect(), if an exception occurs while connecting, tryAgain() will be
        called to re-prompt the user and ask if they want to try again. If they say yes, the loop will continue. If they
        say no, the program will end. The connection loop continues until a connection is made or until the program
        ends. After a connection is made, sendUsername() is called to initiate exchanging usernames.
        """
        connection = False

        while connection is False:
            try:
                self.connect()
                connection = True
                self.sendUsername()

            except:
                self.tryAgain()

    def tryAgain(self) -> None:
        """A function to re-prompt the user after the connection attempt fails.

        Until the user enters a valid input, the program continues to loop. If the user enters 'y', the loop is broken
        and returns to the connection loop in attemptConnection(). If the user inputs 'n', the program quits.
        """

        while True:
            try_again = input("Connection Failed. Would you like to try again? (y/n)\n")
            if (try_again == "y") or (try_again == "Y"):
                break

            if (try_again == "n") or (try_again == "N"):
                quit()
    def sendUsername(self) -> None:
        """A function to exchange usernames between players 1 and 2.

        Continues to loop until a valid alphanumeric username is inputted for player 1. After a valid username is
        inputted, the username is sent to Player 2, and the username of player 2 is received. Both usernames are then
        displayed on the screen.
        """
        invalid_user = True
        while invalid_user is True:
            self.p1username = input("Please enter an alphanumeric username for Player 1:\n")

            if self.p1username.isalnum():
                invalid_user = False

        self.sendData(self.p1username)
        print("\nPlayer 1:", self.p1username)
        self.p2username = self.receiveData()
        print("Player 2:", self.p2username)
        print()

    def sendData(self, data: str) -> None:
        """A function to send data strings to player 2.

        Uses player 1's socket to encode and send data to player 2.

        Args:
            data: a string to send to player 2.
        """
        self.p1socket.sendall(data.encode())

    def receiveData(self) -> str:
        """A function to receive data from player 2.

        Uses player 1's socket to receive and decode data strings from player 2.

        Returns:
            a string containing data sent from player 2.
        """
        return self.p1socket.recv(1024).decode()

    def playerMove(self) -> tuple[int, int]:
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

    def checkMove(self) -> tuple[int, int]:
        """A function to prompt player 1 to enter their move and checks the input for validity.

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
                decoded_move = p1board.decodeMove(int(move))
                row = int(decoded_move[0])
                column = int(decoded_move[1])

                # checks if space has not already been taken
                if p1board.gameboard[row][column] == " ":
                    valid_move = True
                else:
                    print("Invalid input, try again.\n")
                    valid_input = False

            else:
                print("Invalid input, try again.\n")

        return row, column

    def receiveMove(self) -> str:
        """A function to receive a move from player 2.

        Calls the receiveData() function to receive the move player 2 made, and prints it.

        Returns:
            move: the space player 2 inputted that designates where they chose to move.
        """
        print("\nWaiting for Player 2 to move...")
        move = self.receiveData()

        print()
        print("Player 2's move:")
        return move

    def startGame(self) -> None:
        """A function to start a game between player 1 and 2.

        Indicates that a game has started by printing 'Game Start' and calls the resetGameBoard() function to clear
        the board of all moves and calls updateGamesPlayed() to increment the number of games played for the stats.
        """
        print("Game Start")
        p1board.resetGameBoard()
        p1board.updateGamesPlayed()

    def endGame(self, outcome: str) -> None:
        """A function to end the game once an outcome has been found.

        Based on the outcome of the game designated by the argument, prints the result, and increments the number of
        wins or losses for player 1. Calls playAgain() function to prompt player 1 if they would like to play again. If
        the program has not quit after playAgain() is called, then a new game is started by calling startGame().

        Args:
            outcome: a string that dictates the result of the game, which is either a tie, a win, or a loss for
            player 1.
        """
        if outcome == "tie":
            print("Tied Game\n")
        elif outcome == "win":
            print("You Win!\n")
            p1board.num_wins += 1
        elif outcome == "loss":
            print("You Lose\n")
            p1board.num_losses += 1

        self.playAgain()
        self.startGame()

    def playAgain(self) -> None:
        """A function to prompt the user if they would like to play again.

        Loops until 'y' or 'n' is inputted. If the user inputs 'y', then 'Play Again' is sent to player 2. The loop is
        broken and startGame() is called in endGame() function. If the user inputs 'n', then 'Fun Times' is sent to
        player 2.
        """

        while True:
            play_again = input("Play Again? (y/n)\n")
            if (play_again == "y") or (play_again == "Y"):
                self.sendData("Play Again")
                break

            if (play_again == "n") or (play_again == "N"):
                self.sendData("Fun Times")
                p1board.printStats()
                quit()

    def checkBoard(self, symbol: str) -> bool:
        """A function to check if the board for a winning pattern or to check if the board is full.

        Calls isWinner() for each player to see if either player has won, and calls boardIsFull() to check for ties. In
        all winning or tie outcomes, calls endGame() with corresponding outcome if a win or tie is detected.

        Returns:
            True if a win or a tie is detected.
        """

        if p1board.isWinner(symbol) is True:
            if symbol == player1.p1symbol:
                player1.endGame("win")
                return True
            if symbol == player1.p2symbol:
                player1.endGame("loss")
                return True
        if p1board.boardIsFull() is True:
            player1.endGame("tie")
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
            player1_move = self.playerMove()
            # update last player
            p1board.last_player = self.p1username
            # update gameboard
            p1board.updateGameBoard(player1_move, self.p1symbol)
            # check board for wins or ties
            if self.checkBoard(self.p1symbol) is True:
                restart_loop = True

            if restart_loop is False:
                # Player 2 turn
                player2_move = self.receiveMove()
                # update last player
                p1board.last_player = self.p2username
                # update gameboard
                p1board.updateGameBoard(player2_move, self.p2symbol)
                # check board for wins or ties
                self.checkBoard(self.p2symbol)


if __name__ == "__main__":
    player1 = Player1()
    player1.attemptConnection()

    p1board = Boardclass(current_player=player1.p1username, player_symbol=player1.p1symbol,
                         other_symbol=player1.p2symbol)

    player1.startGame()
    player1.runGame()

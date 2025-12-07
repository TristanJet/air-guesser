import random

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.iguess = 0
        self.scores = []

    def addScore(self, score: int):
        self.scores.append(abs(score))

class Game:
    """
    global state of the game, active players, rounds, and the current status

    """
    def __init__(self):
        self.ndist = 10     # Number of distances/rounds per game
        self.dist = []
        self.sumdist = 0
        self.fin = True     # True = Game over/Not started. False = Game running.
        self.players = {}
        self.lb = []    # Leaderboard

    def newGame(self):
        self.fin = False

    def checkSesh(self, id: int) -> bool:
        print(f"Checking: {id}")
        return id in self.players.keys()

    def createPlayer(self, n) -> int:
        """
        Registers a new player into the game.
        Args:
            n: Name of the player
        Returns:
            id: The generated 5-digit ID for the player
        """
        id = genId()
        # SQL STUFF HERE
        self.players[id] = Player(n, id)
        self.fin = False
        return id

    def handleGuess(self, g) -> tuple:
        return (0, self.fin)

def genId() -> int:
    return random.randint(10000, 99999)

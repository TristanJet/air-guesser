import random
import db
from geopy.distance import geodesic

class App:
    def __init__(self):
        db.connect()
        self.players = {}
        self.lb = []

    def checkSesh(self, id: int) -> bool:
        print(f"Checking: {id}")
        return id in self.players.keys()

    def createPlayer(self, n: str) -> int:
        id = genId()
        self.players[id] = Player(n, id)
        return id

class Game:
    '''Initialized on start and not mutated afterwards'''

    nq = 8
    interval = 360 // nq
    def __init__(self):
        self.airports = []
        self.dist = []
        self.sumdist = 0
        self.fin = True

    def start(self):
        self.fin = False
        self.airports, self.dist = airportDistance(Game.interval)
        self.sumdist = sum(self.dist)


class Player:
    '''Player id, name + mutable game state'''

    def __init__(self, name, id):
        self.name = name
        self.id = id

        self.iq = 0
        self.scores = []
        self.total_score = 0
        self.game = Game()

    def handleGuess(self, g) -> tuple:
        return (0, self.game.fin)

    def addScore(self, score: int):
        self.scores.append(abs(score))

def genId() -> int:
    return random.randint(10000, 99999)

def airportDistance(intv: int) -> tuple:
    distances = []
    airports = []

    min = -180
    max = min + intv

    countries = db.getCountriesInRange(min, max)
    queried = db.getAirports(random.choice(countries), min, max)
    ap = [random.choice(queried), None]
    airports.append(ap[0])
    while max != 180:
        min += intv
        max += intv

        countries = db.getCountriesInRange(min, max)
        queried = db.getAirports(random.choice(countries), min, max)
        ap[1] = random.choice(queried)

        current = (ap[0][3], ap[0][4])
        next = (ap[1][3], ap[1][4])
        d = int(geodesic(current, next).kilometers)
        distances.append(d)
        airports.append(ap[1])
        ap[0] = ap[1]

    return airports, distances

def test():
    db.connect()
    ap, d = airportDistance(Game.interval)
    for x in ap:
        print(x)
    print("----------------")
    for x in d:
        print(x)
    i = 0
    while i + 1 < Game.nq:
        print(f"1: {ap[i][0]} 2: {ap[i+1][0]}")
        print(geodesic((ap[i][3], ap[i][4]), (ap[i+1][3], ap[i+1][4])).kilometers)
        i += 1


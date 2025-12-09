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
        self.airports = [] # Each airport is a tuple: (name, country, ?municipality, lat, long)
        self.dist = []
        self.sumdist = 0
        self.fin = True

    def start(self):
        self.fin = False
        self.airports, self.dist = airportDistance(Game.interval)
        self.sumdist = sum(self.dist)

    def airportCoords(self) -> list[tuple]:
        out = []
        for x in self.airports:
            out.append((x[3], x[4]))
        return out


class Player:
    '''Player id, name + mutable game state'''

    def __init__(self, name, id):
        self.name = name
        self.id = id

        self.ig = 0
        self.game = Game()
        self.diffs = []
        self.sumdiffs = 0

    def handleGuess(self, g: int) -> tuple:
        reald = self.game.dist[self.ig]
        diff = abs(g - reald)
        self.diffs.append(diff)
        self.ig += 1
        self.game.fin = self.ig == len(self.game.dist)
        return (diff, reald, sum(self.diffs), self.game.fin)

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
    player = Player("Tristan", 1234)
    player.game.start()
    print(player.game.dist)
    print("----------------")
    g = 3000
    r = player.handleGuess(g)
    print(g)
    print(r)
    g = 5000
    r = player.handleGuess(g)
    print(g)
    print(r)
    g = 2000
    r = player.handleGuess(g)
    print(g)
    print(r)

test()


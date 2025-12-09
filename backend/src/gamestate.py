import random
import db
from geopy.distance import geodesic

class App:
    '''Data with a lifetime of the app'''

    def __init__(self):
        db.connect()
        self.players: dict[int, Player] = {}
        self.lb: list[tuple] = []

    def checkSesh(self, id: int) -> bool:
        print(f"Checking: {id}")
        return id in self.players.keys()

    def createPlayer(self, n: str) -> int:
        id = genId()
        self.players[id] = Player(n, id)
        return id

    def addLeaderboard(self, id: int):
        player = self.players.get(id)
        if player == None: raise Exception
        self.lb.append((id, player.name, player.sumdiffs))
        self.lb.sort(key=lambda x: x[2])
        return

    def getLeaderboard(self) -> list[dict]:
        out = []
        i = 0
        while i < len(self.lb):
            out.append({
                self.lb[i][1]:self.lb[i][2] 
            })
            i += 1
        return out

    def resetPlayerGame(self, id: int) -> bool:
        """Reset player's game state for a new round"""
        player = self.players.get(id)
        if player is None:
            return False
        player.resetGame()
        return True

class Game:
    '''Initialized on start and not mutated afterwards'''

    nq = 8 # Number of questions per game
    interval = 360 // (nq + 1)
    def __init__(self):
        self.airports: list[tuple] = [] # Each airport is a tuple: (name, country, ?municipality, lat, long)
        self.dist: list[int] = []
        self.sumdist = 0

    def start(self):
        self.airports, self.dist = airportDistance(Game.interval)
        self.sumdist = sum(self.dist)

    def airportData(self) -> list[dict]:
        out = []
        i = 0
        while i+1 < len(self.airports):
            c = self.airports[i]
            n = self.airports[i+1]
            out.append({
                "airports": [
                    {
                        "name": c[0],
                        "country": c[1],
                        "lat": c[3],
                        "long": c[4],
                    },
                    {
                        "name": n[0],
                        "country": n[1],
                        "lat": n[3],
                        "long": n[4],
                    }
                ],
            })
            i += 1
        return out


class Player:
    '''Player id, name + mutable game state'''

    def __init__(self, name, id):
        self.name = name
        self.id = id

        self.ig = 0
        self.game = Game()
        self.diffs: list[int] = []
        self.sumdiffs = 0

    def handleGuess(self, g: int) -> tuple:
        reald = self.game.dist[self.ig]
        diff = abs(g - reald)
        self.diffs.append(diff)
        self.sumdiffs = sum(self.diffs)
        self.ig += 1
        fin = self.ig == len(self.game.dist)
        return (diff, reald, self.sumdiffs, fin)

    def resetGame(self):
        """Reset player state for a new game"""
        self.ig = 0
        self.game = Game()
        self.game.start()
        self.diffs = []
        self.sumdiffs = 0


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
    app = App()
    id1 = app.createPlayer("Tristan")
    id2 = app.createPlayer("Jet")
    p1 = app.players[id1]
    p2 = app.players[id2]
    p1.game.start()
    p2.game.start()
    p1.handleGuess(3000)
    p2.handleGuess(3500)
    r2 = p2.handleGuess(7000)
    r1 = p1.handleGuess(4000)
    if r1[3]: app.addLeaderboard(id1)
    if r2[3]: app.addLeaderboard(id2)
    print(app.getLeaderboard())


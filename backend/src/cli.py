import db
import random
from geopy import distance

dist = distance.distance

def main():
    score = 0
    q = 10
    intv = 360/q
    min = -180
    max = min + intv

    db.connect()
    airports = getAirportsLong(min, max)
    ap = [airportFromRow(random.choice(airports)), None]
    while max != 180:
        min += intv
        max += intv

        airports = getAirportsLong(min, max)
        ap[1] = airportFromRow(random.choice(airports))
        distance = int(dist((ap[0]['lat'], ap[0]['long']), (ap[1]['lat'], ap[1]['long'])).kilometers)

        print(
            f"What is the distance between:\n{ap[0]['name']} - {ap[0]['munic']}, {ap[0]['country']}\nand\n{ap[1]['name']} - {ap[1]['munic']}, {ap[1]['country']}"
        )

        in_dist = int(input(':'))
        print(f"You're guess was {in_dist}\nThe actual distance was: {distance} KM")

        diff = abs(distance - in_dist)
        print(f"You were off by: {diff} KM")

        if diff <= 500:
            score += 2
            print(f"You get two points!")
        elif diff <= 1000:
            score += 1
            print(f"You get one point!")

        ap[0] = ap[1]
        print("------------------")
    print(f"You're final score is {score}")
    db.close()

def getAirportsLong(min, max):
    countries = db.getCountriesInRange(min, max)
    return db.getAirports(random.choice(countries), min, max)

def airportFromRow(row):
    return {
        'name': row[0],
        'country': row[1],
        'munic': row[2],
        'lat': row[3],
        'long': row[4],
    }

if __name__ == "__main__":
    main()

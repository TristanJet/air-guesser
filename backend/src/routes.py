from geopy.distance import geodesic as dist
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Airport, Country
from gamestate import Game
import random

frontend_dir = "../../frontend/"
app = Flask(__name__, template_folder=frontend_dir + "templates/", static_folder=frontend_dir+ "static/")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/flight_game'
db.init_app(app)


cookie_key = "sessionId"
game = Game()

# global min_l, max_l, q, intv
# min_l = -180
# q = 10
# intv = 360/q
# max_l = min_l + intv

def getCountriesInRange(min_l, max_l) -> list:
    countries = db.session.query(Airport.iso_country)\
        .filter(Airport.longitude_deg.between(min_l, max_l))\
        .distinct()\
        .all()
    return list(map(lambda x: x[0], countries))

def getAirports(min_l, max_l):
    countries_codes = getCountriesInRange(min_l, max_l)

    if not countries_codes:
        return []

    selected_country = random.choice(countries_codes)

    airports = db.session.query(
        Airport.iso_country,
        Airport.name,
        Airport.municipality,
        Airport.latitude_deg,
        Airport.longitude_deg,
        Country.name.label('country_name')
    )\
        .join(Country, Airport.iso_country == Country.iso_country)\
        .filter(
            Airport.iso_country == selected_country,
            Airport.longitude_deg.between(min_l, max_l)
        )\
        .order_by(Airport.longitude_deg)\
        .all()

    airports_dict = [
        {
            'name': a[1],
            'municipality': a[2],
            'latitude': a[3],
            'longitude': a[4],
            'country_name': a[5]
        }
        for a in airports
    ]

    return airports_dict 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def play():

    return render_template("game.html")

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

'''All API routes should return JSON'''

@app.route("/api")
def api():
    return {
        "status": "online",
    }, 200

@app.route("/api/airports")
def get_airports():
    min_l = -180
    q = 8
    intv = 360 / q  # 36 degrees
    max_l = min_l + intv

    game_data = []
    airports = getAirports(min_l, max_l)
    ap = [random.choice(airports), None]
    while max_l <= 180:
        # new airports for every slice of the map
        if len(game_data) > 0:
            ap[0] = ap[1]
        airports = getAirports(min_l, max_l)
        
        if len(airports) < 1:
            # If we hit the middle of the ocen with no airports 
            # skip this slice and keep moving East.
            print("skip")
            min_l += intv
            max_l += intv
            continue

        # two unique airports
        ap[1] = random.choice(airports)

        # Calc distance
        if len(game_data) == 0:
            coords_1 = (ap[0]['latitude'], ap[0]['longitude'])
            coords_2 = (ap[1]['latitude'], ap[1]['longitude'])
        distance = int(dist(coords_1, coords_2).kilometers)
 
        result = [{
            "point1": {
                "ap1_name": ap[0]['name'],
                "ap1_country": ap[0]['country_name'],
                "ap1_lat": ap[0]['latitude'],
                "ap1_long": ap[0]['longitude'],
            },
            "point2": {
                "ap2_name": ap[1]['name'],
                "ap2_country": ap[1]['country_name'],
                "ap2_lat": ap[1]['latitude'],
                "ap2_long": ap[1]['longitude'],
            },
            "distance": distance
        }]
      
        game_data.append(result)

        # Update for the next round
        min_l += intv
        max_l += intv
    
    return game_data
    
   

@app.route("/api/auth")
def auth():
    id = request.cookies.get(cookie_key)
    authed = game.checkSesh(int(id)) if id != None else False
    return {
        "isAuthed": authed,
    }, 200 if authed else 401

@app.route("/api/createplayer", methods=["GET", "POST"])
def apiCreatePlayer():
    if request.method != "POST":
        return {
            "message": "invalid method",
        }, 405

    data = request.get_json(silent=True)
    if data == None:
        return {
            "message": "bad media",
        }, 415

    id = request.cookies.get(cookie_key)
    if id != None:
        if game.checkSesh(int(id)):
            return {
                "message": "User already exists",
            }, 400

    name = data.get("uname")
    if name == None:
        return {
            "message": "No Name",
        }, 400

    id = game.createPlayer(name)
    resp = make_response({"message": f"{name} created successfully"}, 201)
    resp.set_cookie(cookie_key, str(id))
    print(f"USER CREATED: {game.players[id].name}")
    return resp

@app.route("/api/distance", methods=["GET", "POST"])
def apiPostDistance():
    if request.method != "POST":
        return {
            "message": "invalid method",
        }, 405

    data = request.get_json(silent=True)
    if data == None:
        return {
            "message": "bad media",
        }, 415

    id = request.cookies.get(cookie_key)
    if id == None or game.checkSesh(int(id)) == False:
        return {
            "message": "Unauthorized",
        }, 401

    guess = data.get("guess")
    if guess == None:
        return {
            "message": "No guess",
        }, 400

    r = game.handleGuess(guess)
    response = {
        "distance": r[0],
        "finished": r[1]
    }

    # way to handle final question to get score
    # DOES NOT WORK we do not have this method Tristan Help!! 
    #if r[1]:
        #response["total_score"] = game.getTotalScore(int(id))

    return response, 200
if __name__ == "__main__":
    app.run(debug=True)
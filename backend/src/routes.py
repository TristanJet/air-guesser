from flask import Flask, request, make_response, render_template
from gamestate import App

frontend_dir = "../../frontend/"
app = Flask(__name__, template_folder=frontend_dir + "templates/", static_folder=frontend_dir+ "static/")

cookie_key = "sessionId"
gapp = App()

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

@app.route("/api/newgame")
def newgame():
    id = request.cookies.get(cookie_key)
    if id == None or gapp.checkSesh(int(id)) == False:
        return {
            "message": "Unauthorized",
        }, 401

    player = gapp.players[int(id)]
    player.game.start()
    return player.game.airportData()

@app.route("/api/auth")
def auth():
    id = request.cookies.get(cookie_key)
    authed = gapp.checkSesh(int(id)) if id != None else False
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
        if gapp.checkSesh(int(id)):
            return {
                "message": "User already exists",
            }, 400

    name = data.get("uname")
    if name == None:
        return {
            "message": "No Name",
        }, 400

    id = gapp.createPlayer(name)
    resp = make_response({"message": f"{name} created successfully"}, 201)
    resp.set_cookie(cookie_key, str(id))
    print(f"USER CREATED: {gapp.players[id].name}")
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
    if id == None or gapp.checkSesh(int(id)) == False:
        return {
            "message": "Unauthorized",
        }, 401

    guess = data.get("guess")
    if guess == None:
        return {
            "message": "No guess",
        }, 400

    try:
        g = int(guess)
    except ValueError:
        return {
            "message": "Invalid guess",
        }, 400

    p = gapp.players[int(id)]
    r = p.handleGuess(g)
    if r[3]: gapp.addLeaderboard(int(id))
    return {
        "guess-diff": r[0],
        "actual-distance": r[1],
        "total-diff": r[2],
        "finished": r[3],
    }, 200

@app.route("/api/leaderboard")
def apiLeaderboard():
    return {
        "sortedLb": gapp.getLeaderboard(),
    }, 200

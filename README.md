# ✈️ Air Guesser

A web-based geography guessing game where players estimate distances between airports around the world. Test your geographic knowledge by guessing the distances between randomly selected airports across different continitudes!

## 🎮 Game Features

- **8 Rounds Per Game**: Each game consists of 8 distance estimation challenges
- **Global Coverage**: Airports are selected from different longitude zones around the world
- **Interactive Map**: Visual D3.js map with zoom controls and airport markers
- **Real-time Scoring**: Track your accuracy with cumulative score tracking
- **Leaderboard**: Compete with other players for the best total score

## 🛠️ Technology Stack

### Backend
- **Python 3.x** with Flask web framework
- **MySQL/MariaDB** for airport and country data
- **GeoPy** for accurate distance calculations using geodesic measurements

### Frontend
- **HTML5/CSS3** for structure and styling
- **JavaScript (ES6+)** for game logic
- **D3.js** for interactive map visualization
- **TopoJSON** for geographical data rendering

### Database
- MySQL connector for Python
- Airport and country data tables with longitude-based indexing

## 📋 Prerequisites

- Python 3.7+
- MySQL or MariaDB server
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd air-guesser
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the database**

Create a `.env` file in the project root with your database credentials:
```env
SQL_HOST=localhost
SQL_PORT=3306
SQL_USER=your_username
SQL_PSWD=your_password
DATABASE=your_database_name
```

4. **Import airport data**

Your MySQL database should have the following tables:
- `airport` table with columns: `name`, `iso_country`, `municipality`, `latitude_deg`, `longitude_deg`
- `country` table with columns: `iso_country`, `name`

## 🎯 How to Run

1. **Start the Flask server**
```bash
python routes.py
```

2. **Open your browser**
Navigate to `http://localhost:5000`

3. **Start playing!**
- Enter your name to create a player session
- Navigate to the game page
- Guess the distance between displayed airports
- Track your score and compete on the leaderboard

## 🎲 Game Rules

1. You'll be shown two airports on the map for each round
2. Estimate the distance between them in kilometers
3. Submit your guess
4. See how close you were to the actual distance
5. Your score is the cumulative difference across all rounds (lower is better!)
6. Complete all 8 rounds to submit your score to the leaderboard

## 🔌 API Endpoints

- `GET /api` - Health check
- `GET /api/auth` - Check authentication status
- `POST /api/createplayer` - Create a new player session
- `GET /api/newgame` - Initialize a new game with airport data
- `POST /api/distance` - Submit a distance guess
- `GET /api/leaderboard` - Retrieve sorted leaderboard

## 🎨 Features in Detail

### Session Management
- Cookie-based session tracking
- Unique player IDs for each session
- Persistent game state per player

### Distance Calculation
- Uses geodesic distance calculation for accuracy
- Accounts for Earth's curvature
- Returns distances in kilometers

### Map Visualization
- Mercator projection for familiar world map view
- Interactive zoom controls (1x to 10x)
- Country tooltips on hover
- Visual connections between airport pairs
- Round-by-round marker history

### Scoring System
- Lower total score is better
- Cumulative difference tracking
- Real-time score updates
- Leaderboard persistence across sessions


## 🙏 Acknowledgments

- D3.js for mapping capabilities
- World Atlas TopoJSON data
- GeoPy for distance calculations

---

**Enjoy testing your geography skills! ✈️🌍**

from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "matches.db"

# ---------- HTML ----------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RACISM RANKED</title>

    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: #0a0f1a;
            color: white;
            text-align: center;
        }

        h1 {
            color: #4da3ff;
            margin-top: 20px;
        }

        .container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            flex-wrap: wrap;
        }

        .box {
            background: #111a2b;
            padding: 20px;
            border-radius: 12px;
            width: 400px;
            box-shadow: 0 0 15px rgba(77,163,255,0.2);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #4da3ff;
            color: black;
            padding: 10px;
        }

        td {
            padding: 10px;
            border-bottom: 1px solid #222;
        }

        a {
            color: #4da3ff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .footer {
            margin-top: 40px;
            color: #555;
            font-size: 13px;
        }
    </style>
</head>

<body>

<h1>⚔ PvP HOUSE</h1>

<div class="container">

    <div class="box">
        <h2>🏆 Leaderboard</h2>
        <table>
            <tr><th>Player</th><th>W</th><th>L</th></tr>
            {% for row in stats %}
            <tr>
                <td><a href="/player/{{row[0]}}">{{row[0]}}</a></td>
                <td>{{row[1]}}</td>
                <td>{{row[2]}}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="box">
        <h2>⚔ Match History</h2>
        <table>
            <tr><th>ID</th><th>Winner</th><th>Loser</th></tr>
            {% for row in matches %}
            <tr>
                <td>#{{row[2]}}</td>
                <td>{{row[0]}}</td>
                <td>{{row[1]}}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

</div>

<div class="footer">
    PvP System • Flask Powered
</div>

</body>
</html>
"""

PROFILE = """
<!DOCTYPE html>
<html>
<head>
    <title>Player</title>
    <style>
        body {
            background: #0a0f1a;
            color: white;
            font-family: Arial;
            text-align: center;
        }

        .card {
            margin-top: 100px;
            background: #111a2b;
            display: inline-block;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(77,163,255,0.2);
        }

        h1 { color: #4da3ff; }
    </style>
</head>
<body>

<div class="card">
    <h1>{{user}}</h1>
    <p>Wins: {{wins}}</p>
    <p>Losses: {{losses}}</p>
    <a href="/">Back</a>
</div>

</body>
</html>
"""

# ---------- DB ----------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS stats (
        user TEXT PRIMARY KEY,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        winner TEXT,
        loser TEXT
    )
    """)

    conn.commit()
    return conn, c

# ---------- ROUTES ----------
@app.route("/")
def home():
    conn, c = get_conn()

    c.execute("SELECT user, wins, losses FROM stats ORDER BY wins DESC")
    stats = c.fetchall()

    c.execute("SELECT winner, loser, id FROM matches ORDER BY id DESC")
    matches = c.fetchall()

    conn.close()

    return render_template_string(HTML, stats=stats, matches=matches)

@app.route("/player/<name>")
def player(name):
    conn, c = get_conn()

    c.execute("SELECT wins, losses FROM stats WHERE user=?", (name,))
    data = c.fetchone()

    conn.close()

    if not data:
        data = (0, 0)

    return render_template_string(PROFILE, user=name, wins=data[0], losses=data[1])

# ---------- RUN (IMPORTANT FOR HOSTING) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

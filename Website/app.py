from flask import Flask, request, jsonify, render_template
from data import users
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

# Filtering function
def in_age_range(user_age, range_str):
    if not range_str:
        return True
    low, high = map(int, range_str.split('-'))
    return low <= user_age <= high


def filter_users(users, subject=None, hobby=None, nationality=None, gender=None, age_range=None):
    results = []
    for user in users:
        if subject and not any(subject.lower() == s.lower() for s in user.favorite_subjects):
            continue
        if hobby and not any(hobby.lower() == h.lower() for h in user.hobbies):
            continue
        if nationality and nationality.lower() != user.nationality.lower():
            continue
        if gender and gender.lower() != user.gender.lower():
            continue
        if not in_age_range(user.age, age_range):
            continue
        results.append(user)
    return results

def get_user(name):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
    conn.close()
    return user

def update_water_points(name, points):
    conn = get_db_connection()
    conn.execute("UPDATE users SET water_points = water_points + ? WHERE name = ?", (points, name))
    conn.commit()
    conn.close()


# Serve HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/virtualrooms')
def virtualrooms():
    return render_template('virtualrooms.html')

# Search API
@app.route('/search', methods=['GET'])
def search_users():
    subject = request.args.get('subject')
    hobby = request.args.get('hobby')
    nationality = request.args.get('nationality')
    gender = request.args.get('gender')
    age_range = request.args.get('ageRange')

    matched = filter_users(users, subject, hobby, nationality, gender, age_range)
    return jsonify([user.__dict__ for user in matched])

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    username = data.get("username")
    points = int(data.get("points", 0))
    update_water_points(username, points)
    return jsonify({"message": "Progress updated!"})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    conn.execute("""
        INSERT OR REPLACE INTO users (name, age, nationality, gender, favorite_subjects, hobbies, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["age"],
        data["nationality"],
        data["gender"],
        ",".join(data["favorite_subjects"]),
        ",".join(data["hobbies"]),
        data["bio"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "User added!"})



@app.route('/room/<username>')
def room(username):
    """Render a shared study room for the given user."""
    return render_template('room.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

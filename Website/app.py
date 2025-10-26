from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from data import users  # your sample users list
from models import UserProfile
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500))
    subjects = db.Column(db.String(200))
    hobbies = db.Column(db.String(200))

# --- Helper functions ---
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

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect')
def connect():
    return render_template('connect.html', users=users)

@app.route('/virtualrooms')
def virtualrooms():
    return render_template('virtualrooms.html')

# --- Signup & Profile ---
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        bio = request.form.get('bio', '')
        subjects = request.form.get('subjects', '')
        hobbies = request.form.get('hobbies', '')

        # Check if username exists
        if User.query.filter_by(username=username).first():
            return "Username already exists"

        # Create new user
        hashed_pw = generate_password_hash(password)
        user = User(
            name=name,
            username=username,
            password_hash=hashed_pw,
            bio=bio,
            subjects=subjects,
            hobbies=hobbies
        )
        db.session.add(user)
        db.session.commit()

        # Set cookie and redirect to profile page
        resp = make_response(redirect(url_for('profile_page', username=username)))
        resp.set_cookie('username', username)
        return resp

    return render_template("signup.html")


@app.route("/create_profile/<username>", methods=["GET", "POST"])
def create_profile(username):
    user = User.query.filter_by(username=username).first()
    if request.method == "POST":
        user.bio = request.form['bio']
        user.subjects = request.form['subjects']  # comma-separated
        user.hobbies = request.form['hobbies']    # comma-separated
        db.session.commit()
        return redirect(url_for('profile_page', username=username))

    return render_template("create_profile.html", user=user)


@app.route("/profile/<username>")
def profile_page(username):
    user = User.query.filter_by(username=username).first()
    current_user = request.cookies.get('username')
    return render_template("profile.html", user=user, username=current_user)


# --- Search API ---
@app.route('/search', methods=['GET'])
def search_users():
    subject = request.args.get('subject')
    hobby = request.args.get('hobby')
    nationality = request.args.get('nationality')
    gender = request.args.get('gender')
    age_range = request.args.get('ageRange')

    matched = filter_users(users, subject, hobby, nationality, gender, age_range)
    return jsonify([user.__dict__ for user in matched])

# --- Progress / Water points ---
@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    username = data.get("username")
    points = int(data.get("points", 0))
    # Implement update_water_points(username, points) if needed
    return jsonify({"message": "Progress updated!"})

# --- Add user API ---
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = UserProfile(
        name=data['name'],
        age=data['age'],
        nationality=data['nationality'],
        gender=data['gender'],
        favorite_subjects=data['favorite_subjects'],
        hobbies=data['hobbies'],
        bio=data['bio']
    )
    users.append(new_user)
    return jsonify({"message": "User added successfully"}), 200

# --- Virtual room ---
@app.route('/room/<username>')
def room(username):
    return render_template('room.html', username=username)

# --- Main ---
if __name__ == "__main__":
    db.create_all()  # creates DB tables if they don't exist
    app.run(debug=True)


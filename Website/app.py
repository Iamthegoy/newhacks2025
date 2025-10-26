from flask import Flask, request, jsonify, render_template
from data import users

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

# Serve HTML
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/room/<username>')
def room(username):
    """Render a shared study room for the given user."""
    return render_template('room.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

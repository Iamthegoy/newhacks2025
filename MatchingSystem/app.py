from flask import Flask, request, jsonify, render_template
from data import users

app = Flask(__name__)

# Filtering function
def filter_users(users, subject=None, hobby=None, nationality=None):
    results = []
    for user in users:
        if subject and subject not in user.favorite_subjects:
            continue
        if hobby and hobby not in user.hobbies:
            continue
        if nationality and nationality != user.nationality:
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
    identity = request.args.get('nationality')
    matched = filter_users(users, subject, hobby, nationality)
    return jsonify([user.__dict__ for user in matched])

if __name__ == '__main__':
    app.run(debug=True)

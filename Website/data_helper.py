import json
from models import UserProfile

def get_data():
    """Read JSON data from a file."""
    with open("data.json", 'r') as file:
        return json.load(file)
    

def save_data(data):
    """Save JSON data to a file."""
    with open("data.json", 'w') as file:
        json.dump(data, file, indent=4)


def check_unique_username(data, username):
    """Check if the username is unique in the data."""
    for user in data:
        if user['name'].lower() == username.lower():
            return False
    return True


def add_user(data, username, password, profile: UserProfile):
    """Add a new user to the data."""
    data.append({
        "username": username,
        "password": password,
        "profile": profile.__dict__
    })


<<<<<<< Updated upstream
def get_user_profile(data, username):
    """Retrieve a user's profile by username."""
    for user in data:
        if user['username'].lower() == username.lower():
            profile_data = user['profile']
            return UserProfile(**profile_data)
    return None

print(get_user_profile(
    get_data(),
    "Jack"
))

# DATABASE RESET SCRIPT
"""
data = get_data()
from data import users
for user in users:
    add_user(data, user.name.lower(), "password123", UserProfile(
=======
data = get_data()
from data import users
for user in users:
    add_user(data, user.name.lower(), user.name, "password123", UserProfile(
>>>>>>> Stashed changes
        user.name, user.age, user.nationality, user.gender, user.favorite_subjects, user.hobbies, user.bio,
        water_points=0
    ))
    
save_data(data)
<<<<<<< Updated upstream
"""
=======
>>>>>>> Stashed changes




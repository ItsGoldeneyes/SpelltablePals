from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_cors import CORS
import time
import uuid
import os

app = Flask(__name__)
CORS(app)

# Configure the database URI for PostgreSQL. Replace the connection details accordingly.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PRIVATE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

class Spelltableusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    custom_format = db.Column(JSONB, nullable=True)
    
class Roleformatting(db.Model):
    role = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    custom_format = db.Column(JSONB, nullable=True)


'''
-----------------
HELPER FUNCTIONS
-----------------
'''

# class GameTracker:
#     def __init__(self):
#         self.pending_games = {}
#         self.processed_games = {}
        
#     def add_game(self, players):
#         for i in self.pending_games.keys():
#             if set(players).issubset(set(self.pending_games[i][0])):
#                 # Remove the pending game
#                 del self.pending_games[i]
#                 # Add the processed game
#                 self.processed_games[i] = [players, time.time()]
#                 return i
        
#         self.pending_games[uuid.uuid4] = [players, time.time()]
        


''' 
-----------------
API ENDPOINTS 
-----------------
'''

@app.route('/user_profiles', methods=['POST'])
def get_user_profile():
    '''
    This function returns the user profiles for the given list of players.
    The request body should be a JSON object with the player names as keys.
    '''

    print("POST: /user_profiles")
    data = request.get_json(force=True)
    player_names = data["players"]
    print("Getting user profiles for: ", ', '.join(player_names))
    print("Session ID: ", data["session_id"])
    
    # Query the database for all players and role formats
    user_profiles = Spelltableusers.query.filter(Spelltableusers.username.in_(player_names)).all()
    role_formatting = Roleformatting.query.all()
    
    users_not_found = [username for username in player_names if username not in [user.username for user in user_profiles]]
    if users_not_found:
        print("Users not found. Adding to database: ", ', '.join(users_not_found))
        for username in users_not_found:
            # Get the max id from Spelltableusers table
            max_id = db.session.query(db.func.max(Spelltableusers.id)).scalar()
            # Add a new entry to Spelltableusers table
            new_user = Spelltableusers(id=max_id+1, username=username, reason=None, role=None, custom_format=None)
            db.session.add(new_user)
            db.session.commit()
            
        # Query the database for all players again
        user_profiles = Spelltableusers.query.filter(Spelltableusers.username.in_(player_names)).all()
    
    # Convert the results to a dict of dictionaries
    user_profiles_dict={}
    
    for user in user_profiles:
        user_profiles_dict[user.username] = {
            'role':user.role, 
            'reason':user.reason, 
            'custom_format': user.custom_format}
        
        # Add custom role formatting if it exists
        for role in role_formatting:
            if user.role == role.role:
                user_profiles_dict[user.username]['custom_format'] = role.custom_format
    
    # Return the user profiles as JSON
    return user_profiles_dict

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
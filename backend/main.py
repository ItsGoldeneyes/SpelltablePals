from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_cors import CORS
import time
import datetime
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
    
class Trackedgames(db.Model):
    game_id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    player_1 = db.Column(db.String(50), nullable=False)
    player_2 = db.Column(db.String(50), nullable=False)
    player_3 = db.Column(db.String(50), nullable=False)
    player_4 = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


''' 
-----------------
API ENDPOINTS 
-----------------
'''

@app.route('/user_profiles', methods=['POST'])
def get_user_profiles_endpoint():
    '''
    This function returns the user profiles for the given list of players.
    The request body should be a JSON object with the player names as keys.
    '''

    data = request.get_json(force=True)
    player_names = data["players"]
    print(f"{data['session_id']}    POST: /user_profiles")
    print(f"{data['session_id']}    Getting user profiles for:", ', '.join(player_names))
    
    game_tracker.add_game(player_names, data['session_id'])
    
    user_profiles = get_user_profiles_helper(player_names)

    return user_profiles


@app.route('/process_games', methods=['POST'])
def process_games_endpoint():
    '''
    This function processes the games in the game tracker and adds them to the database.
    '''

    print("POST: /process_games")
    game_tracker.process_games()
    print("Games processed")
    return {"success":"Success"}

'''
-----------------
HELPER FUNCTIONS
-----------------
'''

def get_user_profiles_helper(player_names):
    
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


class GameTracker:
    def __init__(self):
        # Dicts are of format {session_id: {start_time: time.time(), players: [player1, player2, ...]}
        self.pending_games = {}
        self.finished_games = {}
    
    def add_game(self, players, session_id):
        '''
        Logic to log a new game in pending_games. Games remain in pending_games for 10 mins.
        '''
        # If there is no game for this session, add the game to pending_games
        if session_id not in self.pending_games.keys():
            self.pending_games[session_id] = {'start_time': time.time(), 'players': players}
            print(f"{session_id}    Adding game to pending_games: {', '.join(players)}")
            return True
        else:
            # If the new players are different, compare the start times
            if not set(players).issubset(set(self.pending_games[session_id]['players'])):
                # If the new start time is within 10 mins of the old start time, replace the old session with the new session
                if time.time() - self.pending_games[session_id]['start_time'] < 600:
                    print(f"{session_id}    Replacing game in pending_games: {', '.join(players)}")
                    self.pending_games[session_id] = {'start_time': time.time(), 'players': players}
                    return True
                # If the new start time is more than 10 mins from the old start time, add the new session as a new game and move the old session to finished_games
                else:
                    print(f"{session_id}    Adding game to pending_games: {', '.join(players)}")
                    self.pending_games[session_id] = {'start_time': time.time(), 'players': players}
                    return True
            # If the old players are a subset of new players, replace the old players with new
            else:
                print(f"{session_id}    Replacing game in pending_games: {', '.join(players)}")
                self.pending_games[session_id] = {'start_time': time.time(), 'players': players}
                return True
    
    def process_games(self):
        '''
        Logic to move games from pending_games to finished_games.
        '''
        sessions_to_remove = []
        for session_id, game in self.pending_games.items():
            # If the game has been in pending_games for more than 10 mins, move it to finished_games
            # if time.time() - game['start_time'] > 600:
            if time.time() - game['start_time'] > 5:
                print(f"{session_id}    Moving game to finished_games: {', '.join(game['players'])}")
                self.finished_games[session_id] = game
                sessions_to_remove.append(session_id)
        # Remove the games from pending_games
        for session_id in sessions_to_remove:
            del self.pending_games[session_id]
        
        for session_id, game in self.finished_games.items():
            # For each game in finished games, add it to the database
            print(f"{session_id}    Adding game to database: {', '.join(game['players'])}")
            # Create a uuid for the game
            game_id = str(uuid.uuid4())
            # Fill the players list with None if there are less than 4 players
            while len(game['players']) < 4:
                game['players'].append(None)
            # Add the game to the database
            new_game = Trackedgames(game_id=game_id, 
                                    player_1=game['players'][0], 
                                    player_2=game['players'][1], 
                                    player_3=game['players'][2], 
                                    player_4=game['players'][3], 
                                    timestamp=datetime.datetime.fromtimestamp(game['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
            db.session.add(new_game)
        
        db.session.commit()
        self.finished_games = {}
            
'''
-----------------
START THE SERVER
-----------------
'''

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
    

    
# Initialize the game tracker
game_tracker = GameTracker()
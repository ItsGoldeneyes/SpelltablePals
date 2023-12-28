from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_cors import CORS
import time
import datetime
import uuid
import os


'''
-----------------
SETUP AND DATABASE CONFIGURATION
-----------------
'''

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
    discord_id = db.Column(db.String(50), nullable=True)
    changed_on = db.Column(db.DateTime, nullable=True)
    
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
    Request format:
        {"players": ["player1", "player2", ...]}
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
    Request format:
        {}
    '''

    print("POST: /process_games")
    game_tracker.process_games()
    return {"success":"Success"}


@app.route('/update_pal_profiles', methods=['POST'])
def update_pal_profiles_endpoint():
    '''
    This function updates the user profile for a given player.
    Generally used by the Discord bot to add SpellTable Pals players.
    Request format:
        {"discord_id": {"role": "role", "username": "username"},
        "discord_id": {"role": "role", "username": "username"},
        ...}
    '''
    
    data = request.get_json(force=True)
    print("POST: /update_user_profiles")
    print("Updating user profiles for:", ', '.join(data.keys()))
    
    status = update_pals(data)
    
    return {"status": status}


@app.route('/block_user', methods=['POST'])
def block_user_endpoint():
    '''
    This function submits a block request for a given player.
    Request format:
        {"username": "username", reason: "reason"}
    '''
    
    data = request.get_json(force=True)
    print("POST: /block_user")
    
    status = block_user(data['username'], data['reason'])
    
    return {"status": status}


@app.route('/unblock_user', methods=['POST'])
def unblock_user_endpoint():
    '''
    This function submits an unblock request for a given player.
    Request format:
        {"username": "username"}
    '''
    
    username = request.get_json(force=True)['username']
    print("POST: /unblock_user")
    
    status = unblock_user(username)
    
    return {"status": status}

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


def update_pals(user_profiles):
    '''
    This function updates the user profiles for the given SpellTable Pals players.
    
    user_profiles is a dict of dicts with the following format:
    {discord_id: {role: role, username: username}, ...}
    '''
    pals = Spelltableusers.query.filter(Spelltableusers.discord_id.in_(user_profiles.keys())).all()
    
    for user in user_profiles.keys():
        # If the user is not in the database, add them
        if user not in [pal.discord_id for pal in pals]:
            # If the user's username exists in the database, but does not have a discord_id associated with it, assume this is them
            potential_user = Spelltableusers.query.filter(Spelltableusers.username == user_profiles[user]['username']).first()
            if potential_user and potential_user.discord_id == '':
                print(f"User {user_profiles[user]['username']}'s username found in database. Adding discord_id.")
                potential_user.discord_id = user
                potential_user.changed_on = datetime.datetime.now()
                db.session.commit()
            
            else:
                print(f"User {user_profiles[user]['username']} not found in database. Adding them.")
                max_id = db.session.query(db.func.max(Spelltableusers.id)).scalar()
                
                # If user's username is not unique, add a number to the end of it
                if Spelltableusers.query.filter(Spelltableusers.username == user_profiles[user]['username']).first():
                    user_profiles[user]['username'] = user_profiles[user]['username'] + str(max_id+1)
                
                new_user = Spelltableusers(id=max_id+1, 
                                        username=user_profiles[user]['username'],
                                        role=user_profiles[user]['role'], 
                                        discord_id=user,
                                        changed_on=datetime.datetime.now())
                db.session.add(new_user)
                db.session.commit()
                continue
        
        db_user_profile = Spelltableusers.query.filter(Spelltableusers.discord_id == user).first()
        changed_flag = False
        
        # If the user has a custom role or blocked status, don't update their role
        if user_profiles[user]['role'] != db_user_profile.role:
            if db_user_profile.role not in ['custom', 'blocked']:
                db_user_profile.role = user_profiles[user]['role']
                changed_flag=True
        
        # Usernames should be unique as they correspond to SpellTable usernames.
        # If the username has changed and is not unique, don't update it
        if db_user_profile.username != user_profiles[user]['username']:
            if not Spelltableusers.query.filter(Spelltableusers.username == user_profiles[user]['username']).first():
                db_user_profile.username = user_profiles[user]['username']
                changed_flag=True
        
        # If any values were changed, update the changed_on timestamp
        if changed_flag:
            db_user_profile.changed_on = datetime.datetime.now()
            
        db.session.commit()
    
    return "Success"


def block_user(username, reason):
    '''
    This function blocks a user on SpellTable
    '''
    user = Spelltableusers.query.filter(Spelltableusers.username == username).first()
    if not user:
        print(f"User {username} not found, adding to database")
        max_id = db.session.query(db.func.max(Spelltableusers.id)).scalar()
        new_user = Spelltableusers(id=max_id+1, 
                                username=username,
                                role='blocked', 
                                reason=reason,
                                changed_on=datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return "Success"

    if user.role in ['custom', 'chill', 'council']:
        print(f"User {username} is certified chill, block failed")
        return "Failed: chill"
    
    user.role = 'blocked'
    user.reason = reason
    db.session.commit()
    return "Success"


def unblock_user(username):
    '''
    This function unblocks a user on SpellTable
    '''
    user = Spelltableusers.query.filter(Spelltableusers.username == username).first()
    if not user:
        print(f"User {username} not found, can't unblock")
        return "User not found"

    if user.role not in ['blocked']:
        print(f"User {username} is not blocked, can't unblock")
        return "User not blocked"
    
    user.role = None
    user.reason = None
    db.session.commit()
    return "Success"


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
                # If the new start time is within 20 mins of the old start time, replace the old session with the new session
                if time.time() - self.pending_games[session_id]['start_time'] < 1200:
                    print(f"{session_id}    Replacing game in pending_games: {', '.join(players)}")
                    self.pending_games[session_id] = {'start_time': time.time(), 'players': players}
                    return True
                # If the new start time is more than 20 mins from the old start time, add the new session as a new game and move the old session to finished_games
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
            # If the game has been in pending_games for more than 30 mins, move it to finished_games
            if time.time() - game['start_time'] > 1800:
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
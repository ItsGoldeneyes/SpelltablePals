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
    commander_1 = db.Column(db.String(50), nullable=True)
    commander_2 = db.Column(db.String(50), nullable=True)
    commander_3 = db.Column(db.String(50), nullable=True)
    commander_4 = db.Column(db.String(50), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=True)


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
    # If user is using beta v1, commanders won't be included
    if "commanders" not in data.keys():
        data["commanders"] = []
        
    player_names = data["players"]
    player_commanders = data["commanders"]
    print(f"{data['session_id']}    POST: /user_profiles")
    print(f"{data['session_id']}    Getting user profiles for:", ', '.join(player_names))
    print(f"{data['session_id']}    Player Commanders are:", ', '.join(player_commanders))
    
    add_game(player_names, player_commanders, data['session_id'])
    
    user_profiles = get_user_profiles(player_names)

    dict2 = {}
    for username in user_profiles.keys():
        dict2[username.lower()] = user_profiles[username]
        
    user_profiles = {**dict2, **user_profiles}

    return user_profiles


@app.route('/process_games', methods=['POST'])
def process_games_endpoint():
    '''
    This function processes the games in the game tracker and adds them to the database.
    Request format:
        {}
    '''

    print("POST: /process_games")
    process_games()
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
    
    for discord_id in data.keys():
        data[discord_id]['username'] = data[discord_id]['username'].lower()
    
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
    
    status = block_user(data['username'].lower(), data['reason'])
    
    return {"status": status}


@app.route('/unblock_user', methods=['POST'])
def unblock_user_endpoint():
    '''
    This function submits an unblock request for a given player.
    Request format:
        {"username": "username"}
    '''
    
    username = request.get_json(force=True)['username'].lower()
    print("POST: /unblock_user")
    
    status = unblock_user(username)
    
    return {"status": status}

@app.route('/get_user_stats', methods=['POST'])
def get_user_stats_endpoint():
    '''
    This function returns the stats for a given player.
    Request format:
        {"username": "username"}
    '''
    
    username = request.get_json(force=True)['username'].lower()
    print(f"POST: /get_user_stats {username}")
    
    
    

'''
-----------------
HELPER FUNCTIONS
-----------------
'''

def get_user_profiles(player_names):
    
    # Make player_names lowercase
    player_names = [username.lower() for username in player_names]
    
    # Query the database for all players and role formats
    user_profiles = Spelltableusers.query.filter(Spelltableusers.username.in_(player_names)).all()
    role_formatting = Roleformatting.query.all()
    
    users_not_found = [username for username in player_names if username not in [user.username.lower() for user in user_profiles]]
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
            
            if potential_user == None:
                continue
            
            elif potential_user.discord_id == None:
                print(f"User {user_profiles[user]['username']}'s username found in database. Adding discord_id.")
                potential_user.discord_id = user
                potential_user.changed_on = datetime.datetime.now()
                db.session.commit()
            
            else:
                max_id = db.session.query(db.func.max(Spelltableusers.id)).scalar()
                print(f"User {user_profiles[user]['username']+str(max_id+1)} not found in database.")
                
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
    
    # If there are users that are in the database with a discord_id, but not in the user_profiles list, remove their associated roles.
    # They may have left the server or been kicked.
    for user in pals:
        if user.discord_id not in user_profiles.keys():
            print(f"User {user.username} not found in user_profiles. They may have left the server or been kicked.")
            user.discord_id = ''
            user.role = None
            user.changed_on = datetime.datetime.now()
            db.session.commit()
            
    print("Discord User Profiles Updated")
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


def get_user_stats(username):
    '''
    This function returns the stats for a given player.
    
    
    
    response = f"Stats for {username}: \n\
    **{stats['total_games']}** Games Played \n\
    Most Played Commander: {stats['most_played_commander']} \n\
    Most Played Color: {stats['most_played_color']} \n\
    Most Played Opponent: {stats['most_played_opponent']} \n\
    '''
    # Query games database for all games with username in player_1, player_2, player_3, or player_4
    games = Trackedgames.query.filter(Trackedgames.player_1 == username).all()
    games += Trackedgames.query.filter(Trackedgames.player_2 == username).all()
    games += Trackedgames.query.filter(Trackedgames.player_3 == username).all()
    games += Trackedgames.query.filter(Trackedgames.player_4 == username).all()
    
    print(games)



def add_game(players, commanders, session_id):
    '''
    Logic to log a new game in pending_games. Games remain pending for 20 mins.
    '''
    new_players  = players 
    new_players += [''] * (4 - len(players))
    new_commanders = commanders
    new_commanders += [''] * (4 - len(commanders))
    
    # Select games from trackedgames table where status = pending
    pending_games = Trackedgames.query.filter(Trackedgames.status == 'pending').all()
    
    # If the gameid is not in pending_games, add it and return
    if session_id not in [game.game_id for game in pending_games]:
        print(f"{session_id}    Adding game to pending_games: {', '.join(players)}")
        new_game = Trackedgames(game_id=session_id, 
                                player_1=players[0], 
                                player_2=players[1], 
                                player_3=players[2], 
                                player_4=players[3], 
                                commander_1=commanders[0],
                                commander_2=commanders[1],
                                commander_3=commanders[2],
                                commander_4=commanders[3],
                                start_time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                                status='pending')
        db.session.add(new_game)
        db.session.commit()
        return
    
    game = Trackedgames.query.filter(Trackedgames.game_id == session_id).first()
    
    # If the game has been in pending_games for more than 20 mins, change status to 'finished' and change game_id to a new uuid
    if time.time() - game.start_time.timestamp() > 1200:
        print(f"{session_id}    Game finished")
        game.status = 'finished'
        game.game_id = str(uuid.uuid4())
        print(f"{session_id}    Adding game to pending_games: {', '.join(players)}")
        # create new game with the input players and commanders
        new_game = Trackedgames(game_id=session_id,
                                player_1=players[0], 
                                player_2=players[1], 
                                player_3=players[2], 
                                player_4=players[3], 
                                commander_1=commanders[0],
                                commander_2=commanders[1],
                                commander_3=commanders[2],
                                commander_4=commanders[3],
                                start_time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                                status='pending')
        db.session.add(new_game)
        db.session.commit()
        return
    
    # If the game has been in pending_games for less than 20 mins and the new players or commanders are contained within the set of old players, replace the old game with the new game
    if set(players).issubset(set([game.player_1, game.player_2, game.player_3, game.player_4])) and set(commanders).issubset(set([game.commander_1, game.commander_2, game.commander_3, game.commander_4])):
        print(f"{session_id}    Players and commanders are subsets of old players and commanders. Doing nothing.")
        return
    else:
        print(f"{session_id}    Replacing with new game.")
        game.player_1 = players[0]
        game.player_2 = players[1]
        game.player_3 = players[2]
        game.player_4 = players[3]
        game.commander_1 = commanders[0]
        game.commander_2 = commanders[1]
        game.commander_3 = commanders[2]
        game.commander_4 = commanders[3]
        game.start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return


def process_games():
    '''
    Logic to change the status of games in pending_games to finished.
    '''
    print("Processing games")
    
    # Select games from trackedgames table where status = pending
    pending_games = Trackedgames.query.filter(Trackedgames.status == 'pending').all()
    
    # If the game has been in pending_games for more than 20 mins, change status to 'finished' and change game_id to a new uuid
    for game in pending_games:
        if time.time() - game.start_time.timestamp() > 1200:
            print(f"{game.game_id}    Game finished")
            game.status = 'finished'
            game.game_id = str(uuid.uuid4())
            db.session.commit()
            return
        
    print("No games to process")
            
            
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
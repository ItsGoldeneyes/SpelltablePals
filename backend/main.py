from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configure the database URI for PostgreSQL. Replace the connection details accordingly.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PRIVATE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the models for tables used
class Spelltableusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    custom_format = db.Column(JSONB, nullable=True)
    
class Roleformatting(db.Model):
    role = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    custom_format = db.Column(JSONB, nullable=True)

# Route to get user profiles
@app.route('/user_profiles', methods=['POST'])
def get_user_profile():
    print("POST: /user_profiles")
    data = request.get_json(force=True)
    player_names = list(data)
    print("Getting user profiles for: ", ','.join(player_names))
    
    # Query the database for all players
    user_profiles = Spelltableusers.query.filter(Spelltableusers.username.in_(player_names)).all()
    
    # Query the database of custom role formatting
    role_formatting = Roleformatting.query.all()
    
    users_not_found = [username for username in player_names if username not in [user.username for user in user_profiles]]
    if users_not_found:
        print("Users not found. Adding to database: ", ','.join(users_not_found))
        for username in users_not_found:
            # Add a new entry to Spelltableusers table
            new_user = Spelltableusers(username=username, reason=None, role=None, custom_format=None)
            db.session.add(new_user)
            db.session.commit()
    
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
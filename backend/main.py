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

# Define the model for the blockedUsers table
class Spelltableblocked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    blocked = db.Column(db.Boolean, nullable=False, default=False)
    reason = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    custom_format = db.Column(JSONB, nullable=True)

# Route to get user profiles + blocked users
@app.route('/user_profiles', methods=['POST'])
def get_user_profile():
    print("POST: /user_profiles")
    data = request.form
    player_names = list(data)
    print("Getting user profiles for: ", ','.join(player_names))
    # Query the database for all players
    user_profiles = Spelltableblocked.query.filter(Spelltableblocked.username.in_(player_names)).all()
    
    # Convert the results to a list of dictionaries
    user_profiles_dict={}
    
    for user in user_profiles:
        user_profiles_dict[user.username] = {
            'blocked':user.blocked, 
            'role':user.role, 
            'reason':user.reason, 
            'custom_format': user.custom_format}
        
        # Set custom format for specific roles
        if user.blocked:
            user_profiles_dict[user.username]['custom_format'] = {
                    "color": "red",
                    "fontSize": "1.6em",
                    "fontWeight": "bold",
                    "backgroundColor": "",
                    "textDecoration": "underline",
                    "textTransform": "",
                    "textShadow": "",
                    "textIndent": "",
                    "letterSpacing": "",
                    "lineHeight": "",
                    "wordSpacing": "",
                    "whiteSpace": ""
                    }
        elif user.role == "council":
            user_profiles_dict[user.username]['custom_format'] = {
                    "color": "#edc2f6",
                    "fontSize": "",
                    "fontWeight": "",
                    "backgroundColor": "",
                    "textDecoration": "",
                    "textTransform": "",
                    "textShadow": "",
                    "textIndent": "",
                    "letterSpacing": "",
                    "lineHeight": "",
                    "wordSpacing": "",
                    "whiteSpace": ""
                    }
        elif user.role == "chill":
            user_profiles_dict[user.username]['custom_format'] = {
                    "color": "#89b0ff",
                    "fontSize": "",
                    "fontWeight": "",
                    "backgroundColor": "",
                    "textDecoration": "",
                    "textTransform": "",
                    "textShadow": "",
                    "textIndent": "",
                    "letterSpacing": "",
                    "lineHeight": "",
                    "wordSpacing": "",
                    "whiteSpace": ""
                    }
    
    # Return the user profiles as JSON
    return user_profiles_dict

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
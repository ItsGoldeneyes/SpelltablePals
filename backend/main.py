from flask import Flask, jsonify
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
@app.route('/user_profiles', methods=['GET'])
def get_user_profile():
    # Query the database for all blocked users
    user_profiles = Spelltableblocked.query.all()
    
    # Convert the results to a list of dictionaries
    user_profiles_dict = {user.username: {user.blocked, user.custom_format} for user in user_profiles}
    print(user_profiles_dict)
    # Return the user profiles as JSON
    return jsonify(user_profiles_dict)

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
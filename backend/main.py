from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
print(os.getenv('DATABASE_PRIVATE_URL'))
# Configure the database URI for PostgreSQL. Replace the connection details accordingly.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PRIVATE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the model for the blockedUsers table
class BlockedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

# Route to get blocked users
@app.route('/blocked_users', methods=['GET'])
def get_blocked_users():
    # Query the database for all blocked users
    blocked_users = BlockedUser.query.all()

    # Convert the results to a list of dictionaries
    blocked_users_list = [{'id': user.id, 'username': user.username} for user in blocked_users]

    # Return the blocked users as JSON
    return jsonify(blocked_users_list)

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
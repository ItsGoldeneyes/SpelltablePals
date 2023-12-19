from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

print(os.getenv('RAILWAY_ENV'))
print(os.getenv('database.railway.internal.MARIADB_USER'))
print(os.getenv('database.railway.internal.MARIADB_PASSWORD'))

app = Flask(__name__)

# Configure the database URI for MariaDB. Replace the connection details accordingly.
if os.getenv('RAILWAY_ENV') == 'PROD':
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("database.railway.internal.MARIADB_USER")}:{os.getenv("database.railway.internal.MARIADB_PASSWORD")}@database:3306/your_database_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    quit()

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the model for the blockedUsers table
class BlockedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    blocked = db.Column(db.Boolean, nullable=False)

# Route to get blocked users
@app.route('/blocked_users', methods=['GET'])
def get_blocked_users():
    # Query the database for all blocked users
    with app.app_context():
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
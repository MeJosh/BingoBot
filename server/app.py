from flask import Flask
from routes.content_api import blueprint as api_blueprint
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://bingo_db:27017/bingo_db'  # Update with your MongoDB connection details

# Create a MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Access the database
db = client['bingo']

# Create the "teams" collection
teams_collection = db['teams']

app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

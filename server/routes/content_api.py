from flask import Blueprint, jsonify, request
from pymongo import MongoClient

blueprint = Blueprint('api', __name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['bingo']
teams_collection = db['teams']

@blueprint.route("/info_msg")
def info_msg():
    return jsonify({
        "content": "This is the response from the /api/info_msg route"
    })

@blueprint.route("/teams", methods=["GET", "POST", "PUT", "DELETE"])
def teams():
    if request.method == "GET":
        # Get all teams or a specific team by name
        name = request.args.get("name")
        if name:
            team = teams_collection.find_one({"name": name})
            if team:
                return jsonify(team)
            else:
                return jsonify({"message": "Team not found"}), 404
        else:
            teams = list(teams_collection.find())
            return jsonify(teams)

    elif request.method == "POST":
        # Create a new team
        data = request.json
        team = {
            "name": data["name"],
            "display_name": data["display_name"],
            "members": data["members"],
            "progress": {}
        }
        result = teams_collection.insert_one(team)
        return jsonify({"message": "Team created", "team_id": str(result.inserted_id)}), 201

    elif request.method == "PUT":
        # Update an existing team by name
        name = request.args.get("name")
        data = request.json
        update_data = {
            "display_name": data.get("display_name"),
            "members": data.get("members"),
            "progress": data.get("progress")
        }
        result = teams_collection.update_one({"name": name}, {"$set": update_data})
        if result.modified_count > 0:
            return jsonify({"message": "Team updated"})
        else:
            return jsonify({"message": "Team not found"}), 404

    elif request.method == "DELETE":
        # Delete a team by name
        name = request.args.get("name")
        result = teams_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            return jsonify({"message": "Team deleted"})
        else:
            return jsonify({"message": "Team not found"}), 404

    return jsonify({"message": "Invalid method"}), 400

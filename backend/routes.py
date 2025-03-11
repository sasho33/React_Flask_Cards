from app import app, db
from flask import request, jsonify
from models import Friend

# Get all friends

@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

# Create a friend
@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        print(request.json)
        data = request.json
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing {field} field"}), 400
            
        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        name_for_link = name.replace(" ", "+")

        # fetch avatar imge based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name_for_link}"

        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name_for_link}"
        else:
            img_url = None
        
        new_friend = Friend(name=name, role=role, description=description, gender = gender, img_url=img_url)
        db.session.add(new_friend)  # add new friend to the database
        db.session.commit()  # commit changes
        return jsonify(new_friend.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/api/friends/<int:friend_id>", methods=["DELETE"])
def delete_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message": "Friend deleted"}), 200
    except Exception as e:
        db.session.rollback()   
        return jsonify({"error": str(e)}), 500


@app.route("/api/friends/<int:friend_id>", methods=["PATCH"])
def update_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        data = request.json
        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("description", friend.gender)
        
        db.session.commit()
        return jsonify({"message": "Friend updated"}, friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
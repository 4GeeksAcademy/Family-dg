import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member()
jackson_family.add_member({
    "first_name": "John Jackson",
    "age": 35,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jimmy Jackson",
    "age": 5,
    "lucky_numbers": [1]
})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result["done"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@app.route('/member', methods=['POST'])
def add_member():
    data_new_member = request.json
    if not all(k in data_new_member for k in ("first_name", "age", "lucky_numbers")):
        return jsonify({"error": "Missing required fields"}), 400
    members_update = jackson_family.add_member(data_new_member)
    return jsonify(members_update), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
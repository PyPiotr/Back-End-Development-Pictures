from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# HELPER FUNC
######################################################################

def open_pictures_json():
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "data/pictures.json")
    f = open(path)
    data = json.load(f)
    return data


def update_json(data):
    with open(json_url, "w") as file:
        json.dump(data, file)

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    data = open_pictures_json()
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    pictures = open_pictures_json()
    for picutre in pictures:
        if picutre.get("id") == id:
            return jsonify(picutre)
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = json.loads(request.data)
    print(len(data))
    if not new_picture:
        return {"message": "Invalid input parameter"}, 400

    for ele in data:
        if ele.get("id") == new_picture.get("id"):
            return make_response({"Message": f"picture with id {new_picture.get('id')} already present"}, 302)
    # code to validate new_picture ommited
    data.append(new_picture)
    print(len(data))
    return make_response(new_picture, 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_data = json.loads(request.data)

    if not update_data:
        return {"message": "Invalid input parameter"}, 400
    
    for index, ele in enumerate(data):
        if ele.get("id") == id:
            ele.update(update_data)
            return make_response(data[index], 200)
    
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass

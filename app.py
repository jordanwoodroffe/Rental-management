"""
MP Flask Web App

Creates Flask app and registers database API and website endpoints

"""
import pickle
import os

from flask import Flask, render_template, request, Response
from flask_bootstrap import Bootstrap
from FacialRecognition import FaceDetector
from api import api, db, DB_URI
from website import site
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(site)
app.register_blueprint(api)


@app.route("/encode_user", methods=['POST', 'GET'])
def encode_user():
    """Encodes a user: captures and encodes face from images and stores as a pickle file locally

    Params:
        user_id: id/email of user to encode (i.e. register their face)
        directory: path to directory to take images from

    Returns:
        :class:`flask.Response` object, 200 if successful otherwise returns a corresponding error (400 for missing param)
    """
    user_id = request.args.get('user_id')
    directory = request.args.get('directory')
    if None not in (user_id, directory):
        detector = FaceDetector()
        images = []
        for filename in os.listdir(directory):
            images.append("{}/{}".format(directory, filename))
        print("images: {}".format(images))
        encoding = detector.capture_user(images)
        if encoding is not None:
            pickle.dump(encoding, open("user_data/pickles/{}".format(user_id), "wb"))
            response = Response("Success", status=200)
        else:
            response = Response("Error - unable to capture/encode faces", status=404)
    else:
        response = Response("Error - incorrect request params", status=400)
    return response


@app.route("/get_encoding", methods=['GET'])
def get_encoding():
    """Returns an encoding for a user: stored in user_data/pickles

    Returns:
        data for a user, otherwise None if not found
    """
    user_id = request.args.get('user_id')
    if user_id is not None:
        data = pickle.load(open("user_data/pickles/{}".format(user_id), "rb"))
        return data
    return None


@app.route("/authenticate_encodings", methods=['POST', 'GET'])
def auth_by_face():
    """Used to authenticate a user via facial recognition: compares existing encodings against a new encoding

    Args:
        directory: path to directory to read from
        user_id: username of user

    Returns:
        :class:`flask.Response` with 200 and :class:`FacialRecognition.AbstractFaceDetector.Match` if successful, or 400
        if incorrect request params
    """
    directory = request.args.get('directory')
    user_id = request.args.get('user_id')
    if directory is not None:
        detector = FaceDetector()
        with open("{}/{}".format(directory, user_id), 'rb') as log_pickle:
            login = pickle.load(log_pickle)  # load login encodings
        pickles_dir = "user_data/pickles"
        pickles = {
            filename: pickle.load(open("{}/{}".format(pickles_dir, filename), "rb"))
            for filename in os.listdir(pickles_dir)
        }  # load existing registration encodings
        match = detector.compare_encodings(login_encs=login, saved_encs=pickles)
        if match.user_id is not None:  # found a match
            return Response(match.user_id, status=200)
        return Response("missing param", status=400)
    return Response("missing request param", status=400)


@app.errorhandler(404)
def page_not_found(error):
    """Renders when page is not found"""
    return render_template("404.html"), 404


@app.errorhandler(403)
def access_forbidden(error):
    """Renders when user attempts to access forbidden page"""
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal(error):
    """Renders when server error occurs"""
    return render_template("500.html"), 500


Bootstrap(app)
db.init_app(app)

if __name__ == '__main__':
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(debug=True, host="0.0.0.0")

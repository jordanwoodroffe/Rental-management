import pickle
import os
import shutil

from flask import Flask, render_template, request, Response
from flask_bootstrap import Bootstrap
from FacialRecognition import FaceDetector
from api import api, db, DB_URI, LOCAL_IP
from website import site
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(site)
app.register_blueprint(api)


@app.route("/encode_user", methods=['POST'])
def encode_user():
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
            response = Response("Error - unable to capture/encode faces", status=400)
    else:
        response = Response("Error - incorrect request params", status=400)
    return response


@app.route("/get_encoding", methods=['GET'])
def get_encoding():
    user_id = request.args.get('user_id')
    if user_id is not None:
        data = pickle.load(open("user_data/pickles/{}".format(user_id), "rb"))
        return data
    return None


@app.route("/authenticate_encodings", methods=['POST', 'GET'])
def auth_by_face():
    directory = request.args.get('directory')
    user_id = request.arg.get('user_id')
    if directory is not None:
        images = [pickle.load(open("{}{}".format(directory, user_id), 'rb'))]
        # for filename in os.listdir():
        #     images.append("{}{}".format(directory, filename))
        detector = FaceDetector()
        login = detector.capture_user(images=images)
        pickles_dir = "user_data/pickles"
        pickles = {
            filename: pickle.load(open("{}/{}".format(pickles_dir, filename), "rb"))
            for filename in os.listdir(pickles_dir)
        }
        match = detector.compare_encodings(login_encs=login, saved_encs=pickles)
        if match.user_id is not None:
            return Response(match.user_id, status=200)
        return Response("missing request param", status=400)
    return Response("missing request param", status=400)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def access_forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal(error):
    return render_template("500.html"), 500


Bootstrap(app)
db.init_app(app)

if __name__ == '__main__':
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(debug=True, host="0.0.0.0")

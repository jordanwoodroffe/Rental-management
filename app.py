import pickle

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


@app.route("/encode_user", methods=['POST'])
def encode_user():
    user_id = request.args.get('user_id')
    if user_id is not None:
        detector = FaceDetector()
        encoding = detector.capture_user()
        if encoding is not None:
            pickle.dump(encoding, open("pickles/{}".format(user_id), "wb"))
            return Response("Success", status=200)
        return Response("Error - unable to capture/encode faces", status=400)
    return Response("Error - incorrect request params", status=400)


@app.route("/get_encoding", methods=['GET'])
def get_encoding():
    user_id = request.args.get('user_id')
    if user_id is not None:
        data = pickle.load(open("pickles/{}".format(user_id), "rb"))
        return data
    return None


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
    # app.run(debug=True, host='192.168.1.200')  # use IP of MP: as per forums only has to be accessibly locally
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(debug=True)

import os

from flask import Flask, render_template, request
from flask_restplus import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ohili/PycharmProjects/ufgo_rating/ufgo_rating.db'
api = Api(app)
db = SQLAlchemy(app)


MAX_FILE_SIZE = 1024 * 1024 + 1
file_upload = reqparse.RequestParser()
file_upload.add_argument('file', type=FileStorage, location='files', required=True, help='file')


@api.route('/upload')
class Uploader(Resource):
    @api.expect(file_upload)
    def post(self):
        args = file_upload.parse_args()
        if args['file']:
            destination = os.path.abspath('medias/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            xls_file = os.path.join(destination, 'custom_file_name.xls')
            args['file'].save(xls_file)
        else:
            return 'Fail', 404
        return {'status': 'Done'}


@app.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
        args["method"] = "POST"
    return render_template("index.html", args=args)


if __name__ == '__main__':
    app.run('0.0.0.0', '8000', debug=True)

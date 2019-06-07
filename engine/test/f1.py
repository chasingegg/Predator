from flask import Flask
from flask import request, Response
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/test1/', methods=["GET", "POST"])
def test1():
    print("name:")
    print(request.args.get("name"))
    print(request.args["name"])
    print(request.args)
    print("all:")
    print(json.dumps(request.args))
    return json.dumps(request.args)

@app.route('/image/<imageid>')
def index(imageid):
    with open(("{}.jpg".format(imageid)), 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpg")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
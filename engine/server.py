from flask import Flask
from flask import request
from flask import jsonify
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/keyword/<content>')
def keyword_query(content):
    return 'Keyword_Query %s' % content

@app.route('/question/<content>')
def ques_query(content):
    return 'Ques_Query %s' % content

@app.route('/photo/', methods=['get', 'post'])
def up_photo():
    img = request.files.get

if __name__ == '__main__':
    app.run()

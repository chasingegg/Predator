from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import jieba
import os
import json
import utils
from search import SearchEngine

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
BaikeData = utils.loadBaikeToPandas("../data/baike.csv", "utf-8")
engine = SearchEngine("./config.ini", "utf-8")

# @app.route('/')
# def hello_world():
#     return "Hello World!"

@app.route('/', methods=['GET', 'POST'])
def keyword_query():
    print((request.form))
    keyword = request.form.get("keyword")
    f, score = engine.BM25(keyword)
    ids = [i for i, d in score]
    value = []
    d = dict()
    for id in ids:
        row = json.loads(BaikeData.loc[id].to_json())
        row['id'] = id
        value.append(row)
    d['link'] = value
    print(d)
    return jsonify(d)


# @app.route('/question/<content>')
# def ques_query(content):
#     return 'Ques_Query %s' % content



if __name__ == '__main__':
    jieba.initialize()
    app.run(host="0.0.0.0", port=3003)

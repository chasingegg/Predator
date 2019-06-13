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
ZhidaoData = utils.loadZhidaoToPandas("../data/zhidao.csv", "utf-8")
ImageData = utils.loadImgToPandas("../data/images.csv", "utf-8")
engine = SearchEngine("./config.ini", "utf-8")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def search_images(docs):
    res = []
    for id in docs:
        row = json.loads(ImageData.loc[id].to_json())
        images = row['imglist'].split(',')
        for i in images:
            res.append(i)
    return res

# @app.route('/')
# def hello_world():
#     return "Hello World!"

@app.route('/query', methods=['GET', 'POST'])
def query():
    print((request.form))
    keyword = request.form.get("keyword")
    qa = request.form.get("qa")
    img = request.form.get("img")
    baike = request.form.get("baike")
    value = []
    imgL = []
    d = dict()
    if baike == True:
        f, score = engine.BM25_baike(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 30:
                ids = ids[:30]
            for id in ids:
                row = json.loads(BaikeData.loc[id].to_json())
                row['type'] = 1
                if len(row['text']) > 50:
                    row['text'] = row['text'][:50]
                value.append(row)
            if img == True:
                imgL = search_images(ids)

    if qa == True:
        f, score = engine.BM25_zhidao(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 20:
                ids = ids[:20]
            for id in ids:
                row = json.loads(ZhidaoData.loc[id].to_json())
                row['type'] = 0
                row['text'] = row['text'].strip()
                if (len(row['text'])) > 50:
                    row['text'] = row['text'][:50]
                value.append(row)
    if baike != True and img == True:
        f, score = engine.BM25_baike(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 30:
                ids = ids[:30]
                imgL = search_images(ids)

    d['link'] = value
    d['img'] = imgL
    print(d)
    return jsonify(d)


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    docid = request.form.get('docid')
    dtype = request.form.get('type')
    # baike detail
    if dtype == 1:
        row = json.loads(BaikeData.loc[docid].to_json())
        imgL = search_images([docid])
        row['img'] = imgL
    
    # zhidao data
    if dtype == 0:
        row = json.loads(ZhidaoData.loc[docid].to_json())
        ansStr = row['text'].strip()
        best_start = ansStr.find('最佳答案')
        ans_count = ansStr.find('回答')
        ans_start = 0
        str_list = []
        if ans_count == 0:
            str_list.append(ansStr)
        else:
            for i in range(ans_count):
                ind = ansStr.find('回答', ans_start)
                if is_number(ansStr[ind+2 : ind+3]) == True:
                    if i == 0:
                        str_list.append(ansStr[best_start: ind])
                        ans_start = ind
                    elif i == ans_count -1:
                        str_list.append(ansStr[ans_start: ind])
                        str_list.append(ansStr[ind:])
                    else:
                        str_list.append(ansStr[ans_start: ind])

        row['text'] = str_list                
# @app.route('/question/<content>')
# def ques_query(content):
#     return 'Ques_Query %s' % content



if __name__ == '__main__':
    jieba.initialize()
    app.run(host="0.0.0.0", port=3003)

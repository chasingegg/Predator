from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import jieba
import os
import json
import utils
from search import SearchEngine
from flask import render_template

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

def handle_query(args):
    # print(args)
    keyword = args["q"]
    qa = args["qaSearch"]
    img = args["imageSearch"]
    baike = args["baikeSearch"]
    value = []
    imgL = []
    d = dict()
    if baike == True:
        f, score = engine.BM25_baike(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 20:
                ids = ids[:20]
            No_overlap = set()
            new_id = []
            for id in ids:
                row = json.loads(BaikeData.loc[id].to_json())
                len_b = len(No_overlap)
                No_overlap.add(row['keyword'])
                len_a = len(No_overlap)
                if len_b == len_a:
                    continue
                new_id.append(id)
                row['type'] = 1
                if len(row['text']) > 50:
                    row['text'] = row['text'][:50]
                value.append(row)
            if img == True:
                imgL = search_images(new_id)

    if qa == True:
        f, score = engine.BM25_zhidao(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 20:
                ids = ids[:20]
            No_overlap = set()

            for id in ids:
                row = json.loads(ZhidaoData.loc[id].to_json())
                len_b = len(No_overlap)
                No_overlap.add(row['keyword'])
                len_a = len(No_overlap)
                if len_b == len_a:
                    continue
                row['docid'] = id
                row['type'] = 0
                row['text'] = row['text'].strip()
                if (len(row['text'])) > 50:
                    row['text'] = row['text'][:50]
                value.append(row)

    if img == True and baike != True:
        f, score = engine.BM25_baike(keyword)
        if f > 0:
            ids = [i for i, d in score]
            if f > 20:
                ids = ids[:20]
            No_overlap = set()
            new_id = []
            for id in ids:
                row = json.loads(BaikeData.loc[id].to_json())
                len_b = len(No_overlap)
                No_overlap.add(row['keyword'])
                len_a = len(No_overlap)
                if len_b == len_a:
                    continue
                new_id.append(id)
            imgL = search_images(new_id)

    d['link'] = value
    d['img'] = ["http://10.162.167.234/images/" + imgL[i] for i in range(len(imgL))]
    print(d)
    return d
    
def wiki_content(args):
    row = json.loads(BaikeData.loc[args].to_json())
    imgL = search_images([args])
    if (len(imgL) > 0):
        row['img'] = "http://10.162.167.234/images/" + imgL[0]
    else:
        row['img'] = ""
    print(row['text'])
    return row

def qa_content(args):
    docid = args

    # zhidao data
    row = json.loads(ZhidaoData.loc[docid].to_json())
    ansStr = row['text'].strip()
    print(ansStr)
    best_start = ansStr.find('最佳答案')
    ans_count = ansStr.find('回答')
    ans_start = 0
    str_list = []
    if ans_count == 0:
        str_list.append(ansStr)
    else:
        for i in range(ans_count):
            ind = ansStr.find('回答', ans_start+2)
            if is_number(ansStr[ind+2 : ind+3]) == True:
                if i == 0:
                    str_list.append(ansStr[best_start: ind])
                elif i == ans_count -1:
                    str_list.append(ansStr[ans_start: ind])
                    str_list.append(ansStr[ind:])
                else:
                    str_list.append(ansStr[ans_start: ind])
                ans_start = ind

    row['text'] = str_list   
    return row  
    
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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def keyword_query():
    query = request.form.to_dict()
    for c in ['baikeSearch', 'qaSearch', 'imageSearch']:
        if c in query:
            query[c] = True
        else:
            query[c] = False

    results = handle_query(query)

    # put img on the search result
    have_img = query['imageSearch'] and len(results['img'])

    # initialize for first one
    img_dicts = []
    if have_img:
        tmp = {'class': 'carousel-item active', 'img': []}
        for i in range(len(results['img'])):
            if i != 0 and i % 3 == 0:
                img_dicts.append(tmp)
                tmp = {'class': 'carousel-item', 'img': []}
            tmp['img'].append(results['img'][i])

        if len(results['img']) % 3 != 0:
            img_dicts.append(tmp)

    # build href for each link
    for i in range(len(results['link'])):
        if results['link'][i]['type']:
            results['link'][i]['href'] = '/wiki?docid=' + str(results['link'][i]['docid'])
        else:
            results['link'][i]['href'] = '/qa?docid=' + str(results['link'][i]['docid'])

    return render_template('search.html', keyword=query['q'], check_box=query, have_img=have_img,
                           img_dicts=img_dicts, links=results['link'])


@app.route('/qa', methods=['GET', 'POST'])
def build_qa():
    id = int(request.args.get('docid'))
    result = qa_content(id)
    print(result)
    answers = [{'title': 'Answer ' + str(i), 'content': result['text'][i]} for i in range(len(result['text']))]
    return render_template('QA.html', question=result['keyword'], answers=answers, length=len(answers))


@app.route('/wiki', methods=['GET', 'POST'])
def build_wiki():
    id = int(request.args.get('docid'))
    result = wiki_content(id)
    return render_template('wiki.html', title=result['keyword'], img=result['img'], content=result['text'])


if __name__ == '__main__':
    jieba.initialize()
    app.run(host="0.0.0.0", port=3003)

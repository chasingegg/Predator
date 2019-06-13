import sqlite3
import jieba
import operator
import configparser
import math
import time

class SearchEngine:
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        with open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding']) as f:
            words = f.read()
            self.stop_words = set(words.split('\n'))
        self.conn_baike = sqlite3.connect(config['DEFAULT']['db_path_baike'],check_same_thread=False)
        self.conn_zhidao = sqlite3.connect(config['DEFAULT']['db_path_zhidao'], check_same_thread=False)
        self.N_baike = int(config['DEFAULT']['n_baike'])
        self.N_zhidao = int(config['DEFAULT']['n_zhidao'])
        self.K1_baike = float(config['DEFAULT']['k1_baike'])
        self.K1_zhidao = float(config['DEFAULT']['k1_zhidao'])
        self.B_baike = float(config['DEFAULT']['b_baike'])
        self.B_zhidao = float(config['DEFAULT']['b_zhidao'])
        self.AVG_L_baike = float(config['DEFAULT']['avg_l_baike'])
        self.AVG_L_zhidao = float(config['DEFAULT']['avg_l_zhidao'])

    def __del__(self):
        self.conn_baike.close()
        self.conn_zhidao.close()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # wordcount and total number
    def clean_list(self, seg_list):
        cleaned_dict = dict()
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict 

    def fetch_baike(self, keyword):
        c = self.conn_baike.cursor()
        c.execute('SELECT * FROM baike_postings WHERE term=?', (keyword, ))
        data = c.fetchone()
        c.close()
        return data

    def fetch_zhidao(self, keyword):
        c = self.conn_zhidao.cursor()
        c.execute('SELECT * FROM zhidao_postings WHERE term=?', (keyword, ))
        data = c.fetchone()
        c.close()
        return data

    def BM25_baike(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)  # get query terms
        BM25_scores = dict()

        for term in cleaned_dict.keys():
            r = self.fetch(term)
            if r is None:
                continue
            df = r[1]   # doc nums which contain this term
            w = math.log2((self.N_baike - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                s = (self.K1_baike * tf * w) / (tf + self.K1_baike * (1 - self.B_baike + self.B_baike * ld / self.AVG_L_baike))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key = operator.itemgetter(1), reverse=True)
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return len(BM25_scores), BM25_scores
    
    def BM25_zhidao(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)  # get query terms
        BM25_scores = dict()

        for term in cleaned_dict.keys():
            r = self.fetch(term)
            if r is None:
                continue
            df = r[1]   # doc nums which contain this term
            w = math.log2((self.N_zhidao - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                s = (self.K1_zhidao * tf * w) / (tf + self.K1_zhidao * (1 - self.B_zhidao + self.B_zhidao * ld / self.AVG_L_zhidao))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key = operator.itemgetter(1), reverse=True)
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return len(BM25_scores), BM25_scores


if __name__ == '__main__':
    engine = SearchEngine("./config.ini", "utf-8")
    f, score = engine.BM25_baike("篮球")
    print(f, len(score))
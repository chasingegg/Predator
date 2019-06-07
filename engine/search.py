import sqlite3
import jieba
import configparser
import math

class SearchEngine:
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        with open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding']) as f:
            words = f.read()
            self.stop_words = set(words.split('\n'))
        self.conn = sqlite3.connect(config['DEFAULT']['db_path'])
        self.N = int(config['DEFAULT']['n'])
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])

    def __del__(self):
        self.conn.close()

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

    def fetch(self, keyword):
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term, ))
        return (c.fetchone())

    def BM25(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = dict()

        for term in cleaned_dict.keys():
            r = self.fetch(term)
            if r is None:
                continue
            df = r[1]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key = operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores
import sqlite3
import configparser
import os
import jieba
import utils

class Doc:
    def __init__(self, docid, value, ld):
        self.docid = docid  # id of doc
        self.value = value  # tf
        self.ld = ld        # length of doc, which means the number of words that doc contains
    
    def __repr__(self):
        return (str(self.docid) + '\t' + str(self.value) + '\t' + str(self.ld))


class Index:

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        with open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding']) as f:
            words = f.read()
            self.stop_words = set(words.split('\n'))
        self.postings_lists_baike = dict()
        self.postings_lists_zhidao = dict()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # term frequency and total number of terms
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

    # persist baidu index
    def persist_baidu(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS baike_postings''')
        # term, number of docs, docs of Doc(docid, cleaned_dict, length of doc)
        c.execute('''CREATE TABLE baike_postings
            (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')
        for k, v in self.postings_lists_baike.items():
            doc_list = '\n'.join(map(str, v[1]))
            t = (k, v[0], doc_list)
            c.execute("INSERT INTO baike_postings VALUES(?, ?, ?)", t)
        conn.commit()
        conn.close()

    # persist zhidao index
    def persist_zhidao(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS zhidao_postings''')
        # term, number of docs, docs of Doc(docid, cleaned_dict, length of doc)
        c.execute('''CREATE TABLE zhidao_postings
            (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')
        for k, v in self.postings_lists_zhidao.items():
            doc_list = '\n'.join(map(str, v[1]))
            t = (k, v[0], doc_list)
            c.execute("INSERT INTO zhidao_postings VALUES(?, ?, ?)", t)
        conn.commit()
        conn.close()

    def construct_postlings_lists_baike(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        # read baike data into a list
        files = utils.readBaike(config['DEFAULT']['baike_dir_path'], config['DEFAULT']['doc_encoding'])
        avgLen = 0
        for f in files:
            docid = int(f[0])
            title = f[1]
            body = f[2]
            seg_list = jieba.lcut(title + "。" + body, cut_all=False)
            ld, cleaned_dict = self.clean_list(seg_list)
            avgLen = avgLen + ld
            for k, v in cleaned_dict.items():
                d = Doc(docid, v, ld)
                if k in self.postings_lists_baike:
                    self.postings_lists_baike[k][0] = self.postings_lists_baike[k][0] + 1
                    self.postings_lists_baike[k][1].append(d)
                else:
                    self.postings_lists_baike[k] = [1, [d]] 
        avgLen = avgLen / len(files)
        config.set('DEFAULT', 'avg_l_baike', str(avgLen))
        config.set('DEFAULT', 'N_baike', str(len(files)))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configF:
            config.write(configF)
        self.persist_baidu(config['DEFAULT']['db_path_baike'])

    def construct_postlings_lists_zhidao(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        # read zhidao data into a list
        files = utils.readZhidao(config['DEFAULT']['zhidao_dir_path'], config['DEFAULT']['doc_encoding'])
        avgLen = 0
        for f in files:
            docid = int(f[0])
            title = f[1]
            body = f[2]
            # this line needs to be re-considered
            # seg_list = jieba.lcut(title + "。" + body, cut_all=False)
            seg_list = jieba.lcut(title, cut_all=False)
            ld, cleaned_dict = self.clean_list(seg_list)
            avgLen = avgLen + ld
            docid += 1
            for k, v in cleaned_dict.items():
                d = Doc(docid, v, ld)
                if k in self.postings_lists_zhidao:
                    self.postings_lists_zhidao[k][0] = self.postings_lists_zhidao[k][0] + 1
                    self.postings_lists_zhidao[k][1].append(d)
                else:
                    self.postings_lists_zhidao[k] = [1, [d]] 
        avgLen = avgLen / len(files)
        config.set('DEFAULT', 'avg_l_zhidao', str(avgLen))
        config.set('DEFAULT', 'N_zhidao', str(len(files)))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configF:
            config.write(configF)
        self.persist_zhidao(config['DEFAULT']['db_path_zhidao'])

if __name__ == '__main__':
    IndexManager = Index("./config.ini", "utf-8")
    IndexManager.construct_postlings_lists_baike()
    IndexManager.construct_postlings_lists_zhidao()

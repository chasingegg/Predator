import sqlite3
import configparser
import os
import jieba

class Doc:
    def __init__(self, docid, value, ld):
        self.docid = docid
        self.value = value
        self.ld = ld


class Index:

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        with open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding']) as f:
            words = f.read()
            self.stop_words = set(words.split('\n'))
        self.postings_lists = dict()

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

    def persist(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS postings''')
        c.execute('''CREATE TABLE postings
            (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')
        for k, v in self.postings_lists:
            doc_list = '\n'.join(map(str, v[1]))
            t = (k, v[0], doc_list)
            c.execute("INSERT INTO postings VALUES(?, ?, ?)", t)
        conn.commit()
        conn.close()

    def construct_postlings_lists(self):
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        files = os.listdir(config['DEFAULT']['doc_dir_path'])
        avgLen = 0
        for f in files:
            title = ""
            body = ""
            seg_list = jieba.lcut(title + "。" + body, cut_all=False)
            ld, cleaned_dict = self.clean_list(seg_list)
            avgLen = avgLen + ld
            for k, v in cleaned_dict.items():
                d = Doc(docid, cleaned_dict, ld)
                if k in self.postings_lists:
                    self.postings_lists[k][0] = self.postings_lists[k][0] + 1
                    self.postings_lists[k][1].append(d)
                else:
                    self.postings_lists[k] = [1, [d]] 
        AVG_L = AVG_L / len(files)
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        config.set('DEFAULT', 'N', str(len(files)))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configF:
            config.write(configF)
        self.persist(config['DEFAULT']['db_path'])
import csv 
import sqlite3
import pandas as pd
import json
import os

magic_number = 13182

def addZhidaoIDColumn(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, low_memory=False)#, names=["keyword", "time", "name", "text"])
    # docid = [i for i in range(magic_number, magic_number+len(df))]
    # df.insert(0, 'docid', docid)
    df.drop(['time', 'name'], axis=1, inplace=True)
    df.to_csv(config_path, index=False, header=True)
    
def addBaikeIDColumn(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    docid = [i for i in range(len(df))]
    df.insert(0, 'docid', docid)
    df.to_csv(config_path, index=False, header=True)

def readZhidao(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        return [row for row in csv_reader]

def readBaike(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        return [row for row in csv_reader]

def loadZhidaoToPandas(config_path, config_encoding):
    data_type = {'docid':int, 'keyword':str, 'text':str}
    df = pd.read_csv(config_path, encoding=config_encoding, low_memory=False, dtype=data_type, index_col='docid')
    return df


def loadBaikeToPandas(config_path, config_encoding):
    data_type = {'docid':int, 'keyword':str, 'text':str}
    df = pd.read_csv(config_path, encoding=config_encoding, low_memory=False, dtype=data_type)
    return df

def loadImgToPandas(config_path, config_encoding):
    data_type = {'docid':int, 'imglist':str}
    df = pd.read_csv(config_path, encoding=config_encoding, low_memory=False, dtype=data_type)
    return df

def generateImgMap(baike_path, img_path, config_path, config_encoding):
    files = os.listdir(img_path)
    df_baike = loadBaikeToPandas(baike_path, config_encoding)
    print(len(df_baike))
    res = []
    for i in range(0, len(df_baike)):
        docid = df_baike.iloc[i]['docid']
        title = df_baike.iloc[i]['keyword']
        tmp = []
        for f in files:
            if f[:-6] == title:
                tmp.append(f)
        if len(f) > 0:
            ss = ','.join(tmp)
            res.append([docid, ss])

    with open(config_path, mode='w', encoding=config_encoding) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['docid', 'imglist'])
        writer.writerows(res)
    

if __name__ == '__main__':
    # readBaike("../data/baike.csv", "utf-8")
    # loadBaikeToPandas("../data/baike.csv", "utf-8")
    # addBaikeIDColumn("../data/baike.csv", "utf-8")
    # addZhidaoIDColumn("../data/zhidao.csv", "utf-8")
    # loadZhidaoToPandas("../data/zhidao.csv", "utf-8")
    generateImgMap("../data/baike.csv", "../data/images/images/", "../data/images.csv", "utf-8")
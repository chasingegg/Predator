import csv 
import sqlite3
import pandas as pd
import json

def addBaikeIDColumn(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    df['docid'] = [i for i in range(len(df))]
    df.to_csv(config_path, index=False, header=True)
    
def addBaikeIDColumn(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    df['docid'] = [i for i in range(len(df))]
    df.to_csv(config_path, index=False, header=True)

def readZhidao(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        return [row for row in csv_reader]

def readBaike(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        return [row for row in csv_reader]

def loadZhidaoToPandas(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    df['docid'] = [i for i in range(13182, 13182 + len(df))]
    return df


def loadBaikeToPandas(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    df['docid'] = [i for i in range(len(df))]
    return df
    
if __name__ == '__main__':
    # readBaike("../data/baike.csv", "utf-8")
#     loadBaikeToPandas("../data/baike.csv", "utf-8")
    addBaikeIDColumn("../data/baike.csv", "utf-8")
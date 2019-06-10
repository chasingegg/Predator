import csv 
import sqlite3
import pandas as pd
import json

def readBaike(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        return [row for row in csv_reader]

def loadBaikeToPandas(config_path, config_encoding):
    df = pd.read_csv(config_path, encoding=config_encoding, names=["keyword", "text"])
    # row = df.loc[1]
    # print(row)
    # jsonrow = json.loads(row.to_json())
    # jsonrow['id'] = 1
    # print(jsonrow)
    return df
    
if __name__ == '__main__':
    # readBaike("../data/baike.csv", "utf-8")
    loadBaikeToPandas("../data/baike.csv", "utf-8")
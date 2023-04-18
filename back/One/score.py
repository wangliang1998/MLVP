# -*- coding: UTF-8 -*-
import pandas as pd
import csv
import pymysql

user = "root"
password = "928457"

def score(ch):
    if ch == 'A':
        return 95
    elif ch == 'B':
        return 85
    elif ch == 'C':
        return 75
    else:
        return 65

def func():
    quality = []
    lecture = []
    answer = []
    # 预处理前数据
    #data = pd.read_csv('One/score.csv')
    conn = pymysql.connect(host="localhost", user=user, password=password, database="machine")
    data = pd.read_sql("select * from score",con=conn)
    desc = data.describe()
    data1 = []
    for i, row in desc.iterrows():
        data1.append({'num':str(row[0]), 'name':str(row[1]), 'ppt':str(row[2]),
                      'jiangjie':str(row[3]), 'answer':str(row[4]), 'class':str(row[5])})

    # 进行预处理
    with open(r'One/score.csv', encoding='UTF-8') as f:
        f_csv = csv.reader(f)
        samples = []
        rowCount = 0
        for row in f_csv:
            rowCount += 1
            if rowCount >= 3:
                isBlank = 0
                sample = []
                for i in range(len(row)):
                    if row[i] == '':
                        isBlank = 1
                    if i <= 4 and i >= 2:
                        sample.append(score(row[i]))
                    elif i == (len(row) - 1) and row[i] != '':
                        sample.append(row[i].split('：')[1])
                    else:
                        sample.append(row[i])
                if isBlank == 0:
                    samples.append(sample)
                    # print(sample)
                    quality.append(sample[2])
                    lecture.append(sample[3])
                    answer.append(sample[4])
    # 预处理后数据
    dd = pd.DataFrame(samples)
    desc2 = dd.describe()
    data2 = []
    for i in range(len(desc2)):
        data2.append({'one': str(desc2.iloc[i, 0]), 'two': str(desc2.iloc[i, 1]),
                      'three': str(desc2.iloc[i, 2])})
    # 进行统计
    quality = [quality.count(95), quality.count(85), quality.count(75), quality.count(65)]
    lecture = [lecture.count(95), lecture.count(85), lecture.count(75), lecture.count(65)]
    answer = [answer.count(95), answer.count(85), answer.count(75), answer.count(65)]
    f.close()
    return (quality,lecture,answer,data1,data2)








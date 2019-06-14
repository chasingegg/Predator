#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/5 18:51
# @Author  : Wilson
# @Version : 0.8

#导入库文件
import requests
from bs4 import BeautifulSoup
import time
import re
from lxml import etree
from urllib.parse import quote
import csv
from time import sleep
import sys

#网络请求的请求头
# headers = {
#         'User-Agent': '',
#         'cookie': ''
#         }


def sub_urls(response2):
    sub_urls = []
    # response2 = requests.get(page_url)
    response2.encoding = 'gbk'
    html2 = etree.HTML(response2.text)
    select_sub_urls = html2.xpath('//*[@id="wgt-list"]/dl/dt/a/@href')
    for sel in select_sub_urls:
        sub_urls.append(str(sel))
    # print(sub_urls)
    return sub_urls


def get_answers(sub_url):
    answers = []
    sleep(0.05)
    response3 = requests.get(sub_url)
    response3.encoding = 'gbk'
    html3 = etree.HTML(response3.text)
    raw_best_answer = html3.xpath('//*[contains(@class, "best-text")]/text()')
    # print(raw_best_answer)
    # list joined to string ''.join()
    best = ''.join(raw_best_answer).lstrip("'\n'")
    if len(best) < 5:
        best_answer = '最佳答案：None.'
    else:
        best_answer = '最佳答案：' + ''.join(raw_best_answer).lstrip(
            "'\n'").rstrip() + '. '
    answers.append(best_answer)
    # obtain other answers' xpath elements
    answer_selectors = html3.xpath('//*[contains(@class, "answer-text")]')
    i = 0
    for ans_sel in answer_selectors:
        # extract other answers' text
        i += 1
        raw_ans = ans_sel.xpath('string(.)')
        oth_ans = raw_ans.replace('展开全部', '').strip('\n')
        answers.append(str('回答' + str(i) + ' : ' + oth_ans + '.'))
    # answers = [a for a in answers if len(a) >= 100]
    return answers


#构造爬取函数
def get_page(url, data=None):

    #获取URL的requests
    sleep(0.05)
    wb_data = requests.get(url)
    wb_data.encoding = ('gbk')
    soup = BeautifulSoup(wb_data.text, 'lxml')

    #定义爬取的数据
    titles = soup.select('a.ti')
    answer_times = soup.select('dd.dd.explain.f-light > span:nth-of-type(1)')
    answer_users = soup.select(
        'dd.dd.explain.f-light > span:nth-of-type(2) > a')
    # answers = soup.select('dd.dd.explain.f-light > span:nth-of-type(3) > a')
    agrees = soup.select('dd.dd.explain.f-light > span.ml-10.f-black')
    # answers = soup.select('dd.answer')
    # print(type(answers))
    answers = []
    suburls = sub_urls(wb_data)
    # print(answers)
    # print(suburls)
    # print(len(suburls))
    for urls in suburls:
        ans = get_answers((urls))
        # print(ans)
        strans = ""
        for i in ans:
            if i[0] == '"':
                i = i[1:-2]
            strans += i
        answers.append(strans)

    # agrees.encoding = ('gbk')

    #在获取到的数据提取有效内容
    if data == None:
        for title, answer_time, answer_user, answer, agree in zip(
                titles, answer_times, answer_users, answers, agrees):
            data = [
                title.get_text(),
                answer_time.get_text(),
                answer_user.get_text(),
                answer,
                # agree.get_text()
            ]
            # for i in range(4):
            #     print(data[i])
            # print(type(data[3]))
            # print(data)
            saveFile(data)


#迭代页数
def get_more_page(start, end):
    for one in range(start, end, 10):
        print("processing round " + str(one) + "!===========\n")
        get_page(url + str(one))
        sleep(3)


path = "./zhidao.csv"
out = open(path, 'a', newline='')
csv_write = csv.writer(out, dialect='excel')

#定义保存文件函数


def saveFile(data):
    csv_write.writerow(data)


#主体
#定义爬取关键词、页数
# keyword = input('请输入关键词\n')
# pages = input('请输入页码\n')
key_list = [
    "教授", "经济人物", "主持人", "领导人", "毛泽东", "屈原", "林徽因", "爱因斯坦", "苏轼", "鲁迅", "李清照",
    "杜甫", "朱元璋", "溥仪", "韩信", "马可波罗", "达芬奇", "李白", "关羽", "雷锋", "秦始皇", "武则天",
    "刘备", "毕加索", "莫扎特", "贝多芬", "庄子", "胡适", "马克思", "袁世凯", "诸葛亮", "赵云", "任正非",
    "马云", "马化腾", "刘强东", "雷军", "乔布斯", "唐纳德·特朗普", "蔡徐坤", "黄子韬", "奚梦瑶", "张艺兴",
    "新垣结衣", "周杰伦", "李荣浩", "杨超越", "刘亦菲", "琼瑶", "李可", "宫崎骏", "张爱玲", "金庸", "袁隆平",
    "东野圭吾", "三毛", "刘慈欣"
    '陈伟霆', '鹿晗', '刘诗诗', '张艺兴', '黄子韬', '周笔畅', '黄景瑜', '乔振宇', '刘德华', 'Angelababy',
    '钟丽缇', '易烊千玺', '朱一龙', '周震南', '迪丽热巴', '王劲松', '金晨', '邓伦', '杨幂', '赵丽颖',
    '黄旭熙', '王源', '高圆圆', '宋妍霏', '张嘉倪', '翟煦飞', '李墨之', '王俊凯', '姜鹏', '张雪迎', '苍井空',
    '郑爽', '关晓彤', '霍建华', '胡歌', '张子枫', '雷佳音', '赵磊', '具荷拉', '范冰冰', '焉栩嘉', '郭昶',
    '杨烁', '陈芊芊', '任达华', '刘涛', '周杰伦', '唐嫣', '鞠婧祎', '杨洋', '吴刚', '黄磊', '吴亦凡',
    '杨木华', '林一', '李易峰', '朱亚文', '林书豪', '宋茜'
    "孔子", "孙中山", "邓小平", "蒋介石", "杜甫", "韩愈", "鲁迅", "白居易", "孙权", "陆游", '苏轼',
    '王安石', '周瑜', '华佗', '朱元璋', '司马懿', '墨子', '爱新觉罗', '周恩来', '林彪', '张学良', '林徽因',
    '张爱玲', '宋庆龄', '朱德', '宋美龄', '钱学森', '老舍', '彭德怀', '刘少奇', '袁世凯', '朱自清', '李先念',
    '郭沫若', '张作霖', '霍元甲', '梁启超', '邵逸夫', '杨绛', '钱钟书', '季羡林', '巴金', '沈从文', '陈独秀',
    '梁思成', '聂荣臻', '邓稼先', '李大钊', '齐白石', '金庸', '华罗庚', '蔡锷', '叶圣陶', '张大千', '侯宝林',
    '瞿秋白', '康有为', '闻一多', '陈景润', '周星驰', '刘德华'
]

new_list = [
'成龙',
'李连杰',
'习近平',
'潘石屹',
'姜海',
'庞青年',
'张嘉倪',
'袁奇峰',
'徐熙媛',
'李克强',
'斯嘉丽',
'欧阳娜娜',
'林心如',
'杜鹃',
'陈法蓉',
'奥黛丽·赫本',
'李晨',
'勒布朗'
]
# print(len(star_list))
# 定义将要爬取的URL
k = int(sys.argv[1])
key = new_list[k]
url = 'https://zhidao.baidu.com/search?word=' + key + '&ie=gbk&site=-1&sites=0&date=0&pn='
get_more_page(0, int(20) * 10)

# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2,sys,datetime  # 常用的URL库
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

def getHtml(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    request = urllib2.Request(url=url, headers=header)  # 模拟浏览器进行访问
    response = urllib2.urlopen(request)
    text = response.read()
    return text

def getClass(url, number):
    url = url + str(number)
    res = getHtml(url)
    week_now = int(BeautifulSoup(res, 'html.parser').find("form").contents[7][1:3])
    trs = BeautifulSoup(res, 'html.parser').find(id="stuPanel").table.find_all("tr")

    for index, tr in enumerate(trs):
        if index == 0 or index == 3 or index == 6:
            continue
        tds = tr.find_all("td")
        for i, td in enumerate(tds):
            if i == 0:
                continue
            study = td.find("div")
            if study is None:
                continue
            else:
                # index 是第几节课(1,2,4,5,7,8) ,i 是星期几(1-7) prettify
                if index >= 7:
                    selection = index - 3
                elif index >= 4:
                    selection = index - 2
                else:
                    selection = index - 1
                week = i - 1
                if int(study["zc"][week_now - 1:week_now]) == 1:  # 判断是否是本周
                    WeekList[week][selection]['id'] = study.contents[0]
                    WeekList[week][selection]['name'] = study.contents[2]
                    WeekList[week][selection]['place'] = study.contents[4]
                    WeekList[week][selection]['time'] = study.contents[6]
                    WeekList[week][selection]['desc'] = study.find("span").contents[0]
                    WeekList[week][selection]['zc'] = study["zc"]



WeekList = [[({'id':'','name':'','place':'','time':'','desc':'','zc':''}) for q in range(6)] for p in range(7)]
url = 'http://jwzx.node2.cqupt.co/kebiao/kb_stu.php?xh='
id = '2019210223'
week = int(datetime.datetime.now().strftime("%w")) #现在是星期几
getClass(url,id)#获取下当前的课程列表
line = '\r\n'
j = 0#懒得用函数获取index了
class_total = '明天的课程有:' + line
for Classes in WeekList[week]:
    if Classes['name'] == "":
        continue
    else:
        class_total += Classes['name'] + ' \t' + Classes['place'] + ' \t' + Classes['desc'] + line
        j = j + 1
class_total += '明天共有' + str(j) + '节课,要好好学习哦！' + line
print class_total.encode("utf8")


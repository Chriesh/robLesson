import re
import time
import requests
from bs4 import BeautifulSoup



#————————————————————————————————————————
#查询已选课程
def checkLesson(session, selectedCourses_url, rob_Lesson):
    print('Selected Courses Getting...')
    selected = session.get(selectedCourses_url)
    print('Loading-->')
	#——————————————————————————————————————
	#						文本处理，获取已选课程信息
    bs1bj = BeautifulSoup(selected.text, 'html.parser')
    bs1bj = str(bs1bj)
    selected_html = re.findall('(?<=>).*?(?=<)', bs1bj, re.S)
    selected_html = filter(lambda x: x != '\n', selected_html)
    selected_html = filter(lambda x: x != '', selected_html)
    selected_html = filter(lambda x: x != '\xa0', selected_html)
    selected_html = filter(lambda x: x != '\xa0\r\n\r\n\xa0\r\n\r\n', selected_html)
    selected_html = filter(lambda x: x != '\r\n', selected_html)
    selected_html = list(selected_html)
    L = []
    j = 0
    for i in selected_html:
        if i == '&nbsp;':
            j = 1
        elif i == '\r\n\r\n' or i == '\r\n\r\n' or i == '\r\n   ' or i == '\r\n  ' or i == '\r\n ' or i == '\r\n ' or i == '\xa0培养方案' or i == '\xa0大纲日历':
            laji = 1
        elif j == 1:
            i = i.strip('\r\n\t')
            i = i.strip('\xa0')
            L.append(i)
    L.pop(-2)
    j = []
    i = 0
    k = 0
    str_data = ''
    selected_dict = {}
    for c in L:
        i += 1
        if c == '教室':
            k = 1
        elif k == 1:
            str_data = c
            k = 0
            j.append(i)
        elif c == str_data:
            j.append(i)
    #print(j)
    length_j = len(j)
    #print(length_j)
    for t in range(0, length_j):
        selected_dict[L[j[t]]] = L[j[t]: j[t] + 9]
    length_rob_Lesson = len(rob_Lesson)
    #print(length_rob_Lesson)
    for i in range(0, length_rob_Lesson):
        for t in selected_dict:
            if rob_Lesson[i] == t:
                print(selected_dict[t])
    for t in selected_dict:
        print(selected_dict[t])
	#———————————————————————————————————————
    return selected_dict

#————————————————————————————————————————
#				抓取待选课的信息
def selectLesson(session, select_url, select_data):
    conFlag = 'Connection Failed !'
    while conFlag == 'Connection Failed !':
        selectStep0 = session.get(select_url[0])
        prompted = BeautifulSoup(selectStep0.text, 'html.parser').findAll('strong')
        prompted = str(prompted)
        if(prompted == '[<strong><font color="#990000">对不起、非选课阶段不允许选课</font></strong>]'):
            prompted = re.findall('"#990000">' + '(.*?)' + '</font>', prompted, re.S)
            print(prompted)
        #print(selectStep0.status_code)
        print('Select Lesson Geting...')
        select = session.get(select_url[1], params=select_data)
        #print(select.status_code)#响应状态码
        bs2bj = BeautifulSoup(select.text, 'html.parser')
        if(str(bs2bj.findAll('title')) == '[<title>培养方案开课信息</title>]'):
            conFlag = 'Connection Successful !'
            print(conFlag)
        else:
            conFlag = 'Connection Failed !'
            print(conFlag)
            time.sleep(1)
            print('Loading-->')
            print('——————————————————————————————————————————')

    select_html = re.findall('>' + '(.*?)' + '</td>', select.text, re.S)
    L_seletc = []
    x = 0
    dict_data = {}
    for i in select_html:
        if i.find('&nbsp;') != -1:
            x = 1
        elif x == 1:
            i = i.strip('\r\n\t\t')
            if i.find('\n') == -1:
                L_seletc.append(i)
    L_seletc.pop(0)
    #print(L_seletc)
    length_data = int(len(L_seletc)/10)
    for k in range(0, length_data):
        dict_data[L_seletc[k * 10 + 1]] = L_seletc[k * 10: k * 10 + 10]
    #print(dict_data)
    #for result in dict_data:
    #    print(dict_data[result])
    return dict_data

#————————————————————————————————————————————
#   信息比对，查找未选中的课程
def dataCom(selected, select):
    #print(selected)
    #print(select)
    i = 0
    j = 0
    Unchecked = []
    for i in select:
        k = 0
        for j in selected:
            if i == j:
                k = 1
            else:
                k = k
        if k == 0:
            Unchecked.append(i)
    if '331110014' in Unchecked:#2017.8.27，今年特殊多了一个不能选的体育课课序号为'331110014'
        Unchecked.remove('331110014')
    length_Unchecked = len(Unchecked)
    lessonCapacity = {}
    for i in range(0, length_Unchecked):
        lessonCapacity[Unchecked[i]] = [select[Unchecked[i]][-3], select[Unchecked[i]][-8]]
    #print(Unchecked)
    print('未抽中课程: ', end='')
    print(lessonCapacity)
    print('——————————————————————————————————————————')
    if not Unchecked:
        result = 0
    else:
        result = 1
    return result, lessonCapacity, Unchecked

#——————————————————————————————————————————————————————————————
#			自动选课
def rob(session, lessonCapacity, Unchecked, cookies):

    length_lessonCapacity = len(Unchecked)
    #print(length_lessonCapacity)
    rob_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '46',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookies,
        'Host': '202.194.116.35',
        'Origin': 'http://202.194.116.35',
        'Referer': 'http://202.194.116.35/xkAction.do?actionType=2&pageNumber=-1&oper1=ori',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    }
    rob_Lesson = []
    for i in range(0, length_lessonCapacity):
        #print(lessonCapacity[Unchecked[i]][0])
        if int(lessonCapacity[Unchecked[i]][0]) > 0:
            rob_data = {'kcld': Unchecked[i] + '_' + lessonCapacity[Unchecked[i]][1], 'preActionType': 2,  'actionType': 9}
            print(rob_data)
            rob_url = 'http://202.194.116.35/xkAction.do?kcId=' +  Unchecked[i] + '_' + lessonCapacity[Unchecked[i]][1] + '&preActionType=2&actionType=9'
            rob_html = session.post(rob_url, data=rob_data, headers=rob_headers)
            rob_html = BeautifulSoup(rob_html.text, 'html.parser').findAll('strong')
            rob_html = str(rob_html)
            if (rob_html == '[<strong><font color="#990000">选课成功！</font></strong>, <strong>选择</strong>]'):
                result = re.findall('"#990000">' + '(.*?)' + '</font>', rob_html, re.S)
                print(result)
                rob_Lesson.append(Unchecked[i])
    #print(rob_Lesson)

    return rob_Lesson


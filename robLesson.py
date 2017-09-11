#———————————————————————————————————————————————————————————
#   Program Function: Simulated landing of Yantai University urp comprehensive educational system,
#                     and real-time update of the remaining lessons in the curriculum capacity.
#   Last Update time: 2017.8.28
#   Auther          : Cherish_x
#   Version         : 1.0.1
#   注：仅限学习交流使用，请下载24小时后自觉删除。本工程只是为了学习Python3的第三方库requests。
#       用作它处，后果自负
#———————————————————————————————————————————————————————————
import time
import Function
from Load import analogLand

def robLesson():
    post_url = 'http://202.194.116.35/loginAction.do'
    yzm_url = 'http://202.194.116.35/validateCodeAction.do?random'
    selectedCourses_url = 'http://202.194.116.35/xkAction.do?actionType=6'

    select_data = {'actionType': 2, 'pageNumber': -1, 'oper1': 'ori'}
    select_url1 = 'http://202.194.116.35/xkAction.do'#方案课程选课页面
    select_url0 = 'http://202.194.116.35/xkAction.do?actionType=-1'#待跳转页面
    select_url = [select_url0, select_url1]
    session, cookies, ID = analogLand(post_url, yzm_url)#模拟登陆函数
    result = 1
    rob_Lesson = []
    while result:
        print(ID)
        selected_dict = Function.checkLesson(session, selectedCourses_url, rob_Lesson)#抓取已选课程信息函数

        select_dict = Function.selectLesson(session, select_url, select_data)#抓取待选课程数据函数

        result, lessonCapacity, Unchecked, = Function.dataCom(selected_dict, select_dict)#信息比对，寻找未选中课程

        rob_Lesson = Function.rob(session, lessonCapacity, Unchecked, cookies)#检测课容量，自动选课

        time.sleep(0.3)#延时0.3s


if __name__ == '__main__':
    print('仅限学习交流使用，请下载24小时后自觉删除。')
    print('——————————————————————')
    robLesson()















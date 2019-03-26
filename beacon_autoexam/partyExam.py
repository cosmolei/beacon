import os
import time
import configparser
import json
from beacon_autoexam import ExamRobot
from selenium.webdriver.support.select import Select

print("小程序开始读取相关配置......\n")
#删除日志文件
if os.path.exists("log.log"):
    os.remove("log.log")
##获取题库
print("开始读取题库......\n")
tkdetailList = ExamRobot.getTkList()
if len(tkdetailList) > 0 :
    print("题库读取完成!\n")
else:
    print("题库读取失败，请联系开发人员!\n")
    exit()


#读取settings
config = configparser.ConfigParser()
config.read("settings.conf")
login_url = config.get("default","login_url")
lightTower_url = config.get("default","lightTower_url")
logout_url = config.get("default","logout_url")
answer_long = config.getint("config","answer_long")
overdure = config.getint("config","overdure")
wrong_time = config.getint("config","wrong_time")

print("正在获取人员信息......\n")
file = open('user.json',"rb")
user_data = json.load(file)
print("人员信息获取完成，共获得" + str(len(user_data)) +"条人员信息\n")
print("正在启动答题过程......\n")

for i in range(len(user_data)):
    user_name = user_data[i]['name']
    browser = ExamRobot.getBrowser()
    browser.set_window_size(1024, 768)  # 设定固定大小

    #准备登陆
    browser.get(login_url)
    isLogined = ExamRobot.doTheLogin(browser,user_data[i])
    if isLogined == 0:
        print("人员[" + user_name +"]尝试登陆失败，退出本次答题列表！")
        continue

    #登陆成功继续答题
    print("人员[" + user_name +"]登陆成功！准备进行答题")
    browser.get(lightTower_url)
    elem_formal_button = browser.find_element_by_id('lbuts')
    elem_formal_button.click()
    elem_select_shenfen = browser.find_element_by_id('shenfen')
    #党员选定
    Select(elem_select_shenfen).select_by_value("0")

    elem_confirm_button = browser.find_element_by_id('bts')
    elem_confirm_button.click()
    elem_jihui = browser.find_element_by_css_selector(".l_jihui span")
    jihui_value = int(elem_jihui.get_attribute('innerHTML'))
    if jihui_value > 0:
        print("人员[" + user_name + "]可以答题,跳转答题")
        time.sleep(5)
        elem_formal2_button = browser.find_element_by_id('lbuts')
        elem_formal2_button.click()
        # 考试主要过程
        ExamRobot.autoExam(browser,answer_long,overdure,tkdetailList)
        time.sleep(5)
        ExamRobot.screenshot_maker(browser, user_name)
        print("人员[" + user_name + "]答题完成!")
        ExamRobot.write_log("人员[" + user_name + "]答题完成!")
    else:
        print("人员[" + user_name + "]今天已没有答题机会!")
        ExamRobot.write_log("人员[" + user_name + "]今天已没有答题机会!")
        # 准备退出当前账号
    browser.get(logout_url)
    browser.quit()
print("自动答题结束!\n")
exit()

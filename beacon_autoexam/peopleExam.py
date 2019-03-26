import os
import time
import configparser
import json
from beacon_autoexam import ExamRobot
from selenium.webdriver.support.select import Select

#第一步，声明相关量
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
lightTower_url = config.get("default", "lightTower_url")
answer_long = config.getint("config", "answer_long")
overdure = config.getint("config", "overdure")

print("正在获取人员信息......\n")
file = open('phone.json', "rb")
phone_data = json.load(file)
print("人员信息获取完成，共获得" + str(len(phone_data)) +"条人员信息\n")
print("正在启动答题过程......\n")
for i in range(len(phone_data)):
    browser = ExamRobot.getBrowser()
    browser.implicitly_wait(30)
    browser.set_window_size(1024, 768)  # 设定固定大小
    #手机号
    single_phone = phone_data[i]['phone']
    print("正在为手机号为[" + single_phone +"]的人员做答题准备......")
    # 网页打开准备工作
    browser.get(lightTower_url)
    elem_formal_button = browser.find_element_by_id('lbuts')
    elem_formal_button.click()
    # wait = WebDriverWait(browser, 5)
    elem_select_shenfen = browser.find_element_by_id('shenfen')
    # 群众选定
    Select(elem_select_shenfen).select_by_value("1")
    elem_confirm_button = browser.find_element_by_id('bts')
    elem_confirm_button.click()
    # 群众输入手机号
    elem_phone = browser.find_element_by_id('lshouji')
    elem_phone.send_keys(single_phone)

    elem_cf_button = browser.find_element_by_id('btu')
    elem_cf_button.click()

    elem_jihui = browser.find_element_by_css_selector(".l_jihui span")
    jihui_value = int(elem_jihui.get_attribute('innerHTML'))
    if jihui_value > 0:
        print("人员[" + single_phone + "]可以答题,开始答题")
        elem_formal_button.click()
        ExamRobot.autoExam(browser,answer_long,overdure,tkdetailList)
        # 考试成绩截图
        # wait = WebDriverWait(browser, 5)
        time.sleep(5)
        ExamRobot.screenshot_maker(browser,single_phone)
        print("人员[" + single_phone + "]答题完成!")
        ExamRobot.write_log("人员[" + single_phone + "]答题完成!")
    else:
        ExamRobot.screenshot_maker(browser,single_phone)
        fo = open("log.log", "w")
        print("人员[" +single_phone+ "]今天已没有答题机会")
        ExamRobot.write_log("人员[" +single_phone+ "]今天已没有答题机会")
    # 关闭浏览器
    browser.quit()
print("答题结束!\n")
exit()
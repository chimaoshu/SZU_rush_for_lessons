from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from playsound import playsound
import sys

if __name__ == "__main__":

    USERNAME = 'xxxxx'
    PASSWORD = 'xxxxx'

    driver = webdriver.Chrome()
    
    mode = sys.argv[1]
    
    if mode == 'vpn':
    #有VPN模式

        driver.get('http://bkxk.szu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do')
        time.sleep(1)

        loginName = driver.find_element_by_id('loginName')
        loginName.send_keys( USERNAME )

        loginPwd = driver.find_element_by_id('loginPwd')
        loginPwd.send_keys( PASSWORD )

    elif mode == 'webvpn':
    #webVPN模式

        driver.get('http://bkxk.webvpn.szu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do')
        time.sleep(1)

        loginName = driver.find_element_by_id('username')
        loginName.send_keys( USERNAME )

        loginPwd = driver.find_element_by_id('password')
        loginPwd.send_keys( PASSWORD )

        driver.find_element_by_class_name('auth_login_btn').click()

        loginName = driver.find_element_by_id('loginName')
        loginName.send_keys( USERNAME )

        loginPwd = driver.find_element_by_id('loginPwd')
        loginPwd.send_keys( PASSWORD )
    
    else:
        print('参数%s输入错误'%mode)

    print('请手动登录\n')
    while True:
        try:
            assert '本班课程' in driver.page_source
            print('登陆成功\n')        
            break
        except:
            time.sleep(3)

    #课程id列表 
    course_id_list = []

    print('进入选课界面\n')
    while True:

        print('目前已选id列表：\n',course_id_list)
        id = input('\n请查看f12，复制想选择的课程的id并输入。若已经足够，请输入quit。若输入错误，请输入delete删除上一个输入id\n')
        if id == 'quit':
            break
        elif id == 'delete':
            course_id_list.pop(-1)
        else:
            course_id_list.append(id)

    #这三行是为了打开标签，让确定按钮是可点击的
    course_cards = driver.find_elements_by_xpath("//div[@class='cv-row ']") + driver.find_elements_by_xpath("//div[@class='cv-row cv-active']") + driver.find_elements_by_xpath("//div[@class='cv-row']")
    for course_card in course_cards:
        course_card.click()

    #暂停时间（秒）,自己调
    stop_time = 0.5

    while len(course_id_list) != 0:
        try:
            for course_id in list(course_id_list):

                print('id:%s发送选课请求...\n' %course_id)

                #执行js代码，唤出选课确定按钮
                driver.execute_script('document.getElementById("' + course_id + '_courseDiv").className="cv-course-card cv-setting"')
                time.sleep(0.1)

                #按下确认按钮
                button = driver.find_element_by_xpath("//div[@id='" + course_id + "_courseDiv']/div[@class='cv-operate']/div[2]/button[@class='cv-btn cv-btn-chose']")
                button.click()

                #等待ajax加载
                time.sleep(1)

                #考虑实验课的情况
                try:
                    driver.find_element_by_name('testCourse_radio_0').click()
                    driver.find_element_by_id('testCourse_choice_btn').click()
                except:
                    pass

                #等待ajax加载
                time.sleep(1+stop_time)

                try:
                    sign = driver.find_elements_by_xpath("/html/body/div[@class='bh-tip bh-tip-animate-top-opacity bh-tip-success']/div[@class='bh-card bh-card-lv4']/div[@class='bh-tip-content']").text
                    print('系统消息：%s  选课成功!\n'%sign)

                    #这三行是为了打开标签，让确定按钮find得到
                    course_cards = driver.find_elements_by_xpath("//div[@class='cv-row ']") + driver.find_elements_by_xpath("//div[@class='cv-row cv-active']") + driver.find_elements_by_xpath("//div[@class='cv-row']")
                    for course_card in course_cards:
                        course_card.click()

                    course_id_list.remove(course_id)

                except:
                    try:
                        #获得返回信息框内容             
                        sign = driver.find_element_by_xpath("/html/body/div[@id='cvDialog']/div/div[@class='cv-body']/div").text

                        #等待加载
                        time.sleep(stop_time)

                        #点击确定，去掉框框                    
                        driver.find_element_by_xpath("/html/body/div[@id='cvDialog']/div/div[@class='cv-foot']/div[@class='cv-sure cvBtnFlag']").click()

                        print('选课失败，原因是：%s 正在重试...\n'%sign)                    

                        if '已经存在选课结果' in sign:
                            print('该课程已抢到，无需再抢\n')
                            course_id_list.remove(course_id)

                        #这三行是为了打开标签，让确定按钮可点击
                        course_cards = driver.find_elements_by_xpath("//div[@class='cv-row ']") + driver.find_elements_by_xpath("//div[@class='cv-row cv-active']") + driver.find_elements_by_xpath("//div[@class='cv-row']")
                        for course_card in course_cards:
                            course_card.click()
                
                    except:                     
                          
                        print('可能是选课成功，也可能是网速不好，正在检查状况...\n')
                        time.sleep(stop_time+0.5)
                        try:
                            driver.find_element_by_xpath("/html/body/div[@id='cvDialog']/div/div[@class='cv-foot']/div[@class='cv-sure cvBtnFlag']").click()
                            print('检查完成，选课并没有成功，只是你网速太慢了\n')
                        except:
                            pass
                        
        except:
            playsound('warn.mp3')
            input('\n程序出了点错误...请检查网络，建议尽量使用vpn，若网络没问题，请按enter键继续抢课\n\n')
                      
    print('抢课任务结束\n')          
                


                    










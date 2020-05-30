import time
import random
import ynulogin
import servchan
import datetime
import autorecommend
import autosuxuan
import coursepage


class Ynuxk(object):
    def __init__(self, driversite, user):
        self.driversite = driversite
        self.user = user
        self.error_count = 1
        self.run_count = 0
        now_time = datetime.datetime.now()
        self.log_file_path = 'log\\' + str(now_time.date()) + '.txt'

    def myinit(self):

        initFile = open("configure\\init.txt", 'r', encoding='utf-8')
        initConfig = eval(initFile.read())
        self.users = initConfig['users']
        self.beginTime = initConfig['begintime']
        self.endTime = initConfig['endtime']
        initFile.close()

        changeTimeFile = open("configure\\changetime.txt",
                              'r', encoding='utf-8')
        self.change_minute = int(changeTimeFile.read())
        changeTimeFile.close()

    def run(self):
        self.myinit()

        now_time = datetime.datetime.now()
        now_hour = now_time.hour
        if now_hour >= self.beginTime or now_hour <= self.endTime:
            old_page = 0
            less_sleep = True
            is_update = False
            self.xk_driver = ynulogin.YnuLogin(self.driversite, self.user).uesrlogin()
            servchan.send_msgwc(
                self.users['sckey'], '系统启动', str(datetime.datetime.now()))
            while True:
                # result_text =autorecommend.AutoRecommend(
                #     self.xk_driver).recommends(self.users['recommend'])
                result_text = autosuxuan.AutoSuxuan(self.xk_driver).suxuan(self.users['suxuan'])
                now_page =coursepage.CoursePage(self.xk_driver).getpage()

                now_time = datetime.datetime.now()
                now_minute = now_time.minute
                # global log_file_path
                self.log_file_path = 'log\\' + str(now_time.date()) + '.txt'

                if self.endTime+1 <= now_time.hour <= self.beginTime-1:
                    break
                cha = self.change_minute-now_minute
                if cha < 0:
                    cha = 60-now_minute+self.change_minute

                if less_sleep and (1 < cha < 20):
                    sleeptime = random.uniform(60*cha-110.2, 60*cha-100.5)
                elif less_sleep and abs(now_minute-self.change_minute) <= 1:
                    sleeptime = random.uniform(10.121, 25.412)
                else:
                    sleeptime = random.uniform(910.524, 1150.332)
                    # if(now_minute>=20):
                    less_sleep = True

                if 0 < now_page-old_page < 10 and old_page != 0:
                    self.change_minute = now_minute
                    is_update = True
                    title = '更新 '+str(now_page)+" "+str(old_page)
                else:
                    title = '刷新 '+str(now_page)+" "+str(old_page)
                    if is_update:
                        less_sleep = False
                        is_update = False

                if result_text != '':
                    title = '余课通知'
                    servchan.send_msgwc(
                        self.users['sckey'], title, result_text + '\n' + str(now_time))

                people_num = self.xk_driver.find_element_by_css_selector(
                    '#noline-tip').text
                old_page = now_page
                log_text = str(self.run_count) + ' ' + title + '：'+result_text + ' ' + str(
                    now_time)+' 休眠：'+str(sleeptime)+' '+people_num+' 更新时间：'+str(self.change_minute)
                print(log_text)
                self.run_count += 1
                self.error_count = 1

                changeTimeFile = open(
                    "configure\\changetime.txt", 'w', encoding='utf-8')
                changeTimeFile.write(str(self.change_minute))
                changeTimeFile.close()

                f = open(self.log_file_path, 'a', encoding='utf-8')
                f.write(log_text+'\n')
                f.close()

                time.sleep(sleeptime)
        else:
            if self.xk_driver != None:
                self.xk_driver.close()
            servchan.send_msgwc(self.users['sckey'], '系统关闭', str(now_time))
            longsleeptime = (self.beginTime-now_hour)*3600
            time.sleep(random.uniform(longsleeptime+0.2, longsleeptime+300.8))

    def main(self):
        while True:
            try:
                self.run()
            except Exception as e:
                # self.xk_driver.refresh()
                send_message = str(self.error_count) + '  error  ' + \
                    str(datetime.datetime.now()) + '\n\n' + str(e)
                print(send_message)
                if self.error_count == 4:
                    if self.xk_driver != None:
                        self.xk_driver.close()
                    servchan.send_msgwc(
                        self.users['sckey'], '系统异常关闭', send_message)
                    break
                try:
                    servchan.send_msgwc(
                        self.users['sckey'], '系统关闭异常', send_message)
                    f = open(self.log_file_path, 'a', encoding='utf-8')
                    f.write(send_message + '\n')
                    f.close()
                except Exception as er:
                    print(er)
                self.error_count += 1
                time.sleep(random.uniform(280.121, 320.412))


if __name__ == '__main__':
    driversite = 'D:\\code\\chromedriver.exe'  # 浏览器驱动路径
    user = {'username': '20171120000', 'userpassword': 'pasword',
            'codename': 'yth123456', 'codepassword': 'password', 'codeid': '903265'}
    run1 = Ynuxk(driversite, user)
    run1.main()

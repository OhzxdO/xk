from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import code
from selenium.webdriver.common.action_chains import ActionChains
import time


class YnuLogin(object):
    def __init__(self,driversite,user):
        self.website='http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'
        self.driversite=driversite
        self.username=user['username']
        self.userpassword=user['userpassword']
        self.codename=user['codename']
        self.codepassword=user['codepassword']
        self.codeid=user['codeid']

    # 登录
    def uesrlogin(self):
        chrome_options = Options()
        # 浏览器参数配置
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

        self.driver = webdriver.Chrome(executable_path=self.driversite,chrome_options=chrome_options)

        # 打开chrome浏览器
        # driver = webdriver.Chrome(executable_path=driversite,chrome_options=option)
        # driver = webdriver.Chrome(driversite)
        picture = 'pachongmark.png'
        self.driver.get(self.website)
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.ID, 'loginName')))
        self.driver.find_element_by_id('loginName').send_keys(self.username)
        self.driver.find_element_by_id('loginPwd').send_keys(self.userpassword)
        infotext='first'
        while infotext!='' and infotext!='请填写验证码':
            WebDriverWait(self.driver, 10, 0.5).until(
                EC.presence_of_element_located(
                    (By.ID, 'vcodeImg')))
            mark = self.driver.find_element_by_id('vcodeImg')
            if infotext!='first':
                mark.click()
            link = mark.get_attribute('src')
            print(link)  # 验证码地址
            response = requests.get(link)
            with open(picture, 'wb') as f:
                f.write(response.content)
            f.close()
            chaojiying = code.Chaojiying_Client(self.codename, self.codepassword, self.codeid)
            im = open('pachongmark.png', 'rb')
            result = chaojiying.PostPic(im.read(), 1902)['pic_str']
            im.close()
            print(result)
            vecode=self.driver.find_element_by_id('verifyCode')
            vecode.clear()
            vecode.send_keys(result)
            loginbutton = self.driver.find_element_by_id('studentLoginBtn')
            loginbutton.click()
            info = self.driver.find_element_by_css_selector('#loginDiv > div.cv-btns')
            infotext=info.text
            print(info.text)
        print('登录成功，系统启动')
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#buttons > button.bh-btn.bh-btn.bh-btn-primary.bh-pull-right')))
        sure = self.driver.find_element_by_css_selector('#buttons > button.bh-btn.bh-btn.bh-btn-primary.bh-pull-right')
        sure.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#courseBtn')))
        start = self.driver.find_element_by_css_selector('#courseBtn')
        start.click()
        return self.driver

# if __name__ == '__main__':
#     ynulogin=YnuLogin(website,driversite,username,password)
#     ynulogin.uesrlogin()
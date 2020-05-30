from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class AutoSuxuan(object):
    def __init__(self, driver):
        self.driver = driver

    def suxuan(self, recommendcondition):
        self.driver.refresh()
        # try:
        #     WebDriverWait(driver, 10, 0.5).until(
        #         EC.presence_of_element_located(
        #             (By.CSS_SELECTOR, '#buttons > button')))
        #     sure=driver.find_element_by_css_selector('#buttons > button')
        #     sure.click()
        # except:
        #     print('sure_error')
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#aPublicCourse')))
        selection = self.driver.find_element_by_css_selector('#aPublicCourse')
        selection.click()
        time.sleep(1)
        result_str = ''
        for e in recommendcondition:
            result_str = result_str+self.run(e)
        return result_str

    def run(self, input_group):
        want_course, want_id = input_group
        selectable_course_list = self.findcourse(want_course)
        message = ''
        selet_button_place = 0
        for this_course in selectable_course_list:
            text_list = this_course.text.split('\n')
            if len(text_list) > 1:
                selet_button_place += 1
                course_id = text_list[0]
                select_peolple = float(text_list[7])/float(text_list[6])
                cssSelect = '#publicBody > div:nth-child('+str(
                    selet_button_place)+') > div.cv-setting-col > a'

                if course_id == want_id and select_peolple < 1:
                    WebDriverWait(self.driver, 10, 0.5).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, cssSelect)))
                    choosebutton = self.driver.find_element_by_css_selector(
                        cssSelect)
                    choosebutton.click()

                    WebDriverWait(self.driver, 10, 0.5).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, 'cvBtnFlag')))
                    surebutton = self.driver.find_element_by_class_name(
                        'cvBtnFlag')
                    surebutton.click()
                    message += want_course+' ' + want_id + '\n'

        return message

    def findcourse(self, coursename):
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#publicSearch')))
        inputtext = self.driver.find_element_by_css_selector('#publicSearch')
        time.sleep(0.5)
        inputtext.clear()
        inputtext.send_keys(coursename)
        inputtext.send_keys(Keys.ENTER)
        time.sleep(1)
        selectable_course_list = self.driver.find_elements_by_class_name(
            'cv-row')

        return selectable_course_list

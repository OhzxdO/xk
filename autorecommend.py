from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class AutoRecommend(object):
    def __init__(self,driver):
        self.driver=driver

    def recommends(self, recommendcondition):
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
                (By.CSS_SELECTOR, '#recommend_sfym')))
        selection = self.driver.find_element_by_css_selector('#recommend_sfym')
        selection.click()
        result_str = ''
        for e in recommendcondition:
            result_str=result_str+self.run(e)
        return result_str

    def run(self, input_group):
        want_course,want_teacher,delete_course,delete_teacher = input_group
        selectable_course_list = self.findcourse(want_course)
        message=''
        select_status = 'begin'
        selet_button_place = 0
        while selet_button_place < len(selectable_course_list):
            this_course = selectable_course_list[selet_button_place]
            text_list = this_course.text.split('\n')
            teacher_name = text_list[0]

            if teacher_name == want_teacher and select_status != 'deletingcourse':
                if not text_list.__contains__('人数已满') and not text_list.__contains__('已选') :
                    if delete_course == '' or select_status=='deletedcourse':
                        self.selectcourse(this_course, selet_button_place)
                        return message + want_course+' '+ teacher_name + '\n'
                    elif delete_course != want_course:
                        selectable_course_list = self.findcourse(delete_course)
                    selet_button_place = -1
                    select_status = 'deletingcourse'

            if teacher_name == delete_teacher and select_status == 'deletingcourse':
                self.deletecourse(this_course)
                message = message + delete_course+' '+ teacher_name + '\n'
                self.driver.refresh()
                # try:
                #     WebDriverWait(driver, 10, 0.5).until(
                #         EC.presence_of_element_located(
                #             (By.CSS_SELECTOR, '#buttons > button')))
                #     sure = driver.find_element_by_css_selector('#buttons > button')
                #     sure.click()
                # except:
                #     print('sure_error')
                #                 certainbutton=driver.find_element_by_css_selector('#buttons > button')
                #                 certainbutton.click()
                selectable_course_list = self.findcourse(want_course)
                select_status = 'deletedcourse'
                selet_button_place = -1
            selet_button_place += 1
        return message


    def findcourse(self, coursename):
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#recommendSearch')))
        inputtext = self.driver.find_element_by_css_selector('#recommendSearch')
        inputtext.clear()
        inputtext.send_keys(coursename)
        inputtext.send_keys(Keys.ENTER)
        time.sleep(1)
        di = self.driver.find_element_by_class_name('cv-row')
        di.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cv-course-card')))
        selectable_course_list = self.driver.find_elements_by_class_name('cv-course-card')

        return selectable_course_list


    def selectcourse(self, course, selet_button_place):
        course.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cv-btn-chose')))
        choosebutton = self.driver.find_elements_by_class_name('cv-btn-chose')
        choosebutton[selet_button_place].click()


    def deletecourse(self, course):
        course.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cv-delete-volunteer')))
        deletebutton = self.driver.find_element_by_class_name('cv-delete-volunteer')
        deletebutton.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cvBtnFlag')))
        surebutton = self.driver.find_element_by_class_name('cvBtnFlag')
        surebutton.click()

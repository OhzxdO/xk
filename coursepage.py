from selenium.webdriver.support.select import Select
import random
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CoursePage(object):
    def __init__(self,driver):
        self.driver=driver

    def getpage(self):
        selection = self.driver.find_element_by_css_selector('#aPublicCourse')
        selection.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#public_sfym')))
        se = Select(self.driver.find_element_by_css_selector('#public_sfym'))
        se.select_by_value("0")
        time.sleep(2)
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#publicTotalPage')))
        page = self.driver.find_element_by_css_selector('#publicTotalPage').text
        return int(page)


import os.path
import time

import pywinauto
import undetected_chromedriver as ucd
from pywinauto.keyboard import send_keys
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.service import Service


PIC_PATH = r"C:\THE_PATH_TO_SAVE"


def prepare_driver(url):
    ret = ucd.Chrome()
    ret.maximize_window() 
    ret.get(url) 
    return ret


def reset(driver):
    email_input = driver.find_element(By.XPATH, '//input[@name="email"]')
    email_input.send_keys('yourname@email.com')
    time.sleep(2)
    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys("y0ur_passw0rd")
    time.sleep(2)
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()
    time.sleep(5)
    driver.get("https://www.tumblr.com/ACCOUNT_YOU_WANNA_SCRAP")
    time.sleep(10)
    continue_button = driver.find_element(By.XPATH, '//button[text()="ブログを表示"]')
    continue_button.click()
    # Wait for page loading complete
    time.sleep(30)


def find_pics(driver):
    count = 0

    while True:
        imgs = driver.find_elements(By.XPATH, '//div[@data-testid]//button/span/figure/div/img')
        print(len(imgs))
        try:
            img = imgs[count]
            actions = ActionChains(driver)
            actions.move_to_element(img)

            actions.context_click(img)
        

            # ZOOMED
            # actions.click(img)
            # actions.perform()
            # time.sleep(2)
            # actions = ActionChains(driver)
            # zoomed_img = driver.find_elements(By.XPATH, '//button[@aria-label="画像を閉じる"]/span/img')
            # actions.move_to_element(zoomed_img)
            # actions.context_click(zoomed_img)
            
            actions.perform()
            time.sleep(1)
            send_keys('v')

            # save by pywinauto
            app = pywinauto.Desktop()
            dialog = app['另存为']
            time.sleep(1)
            dialog['Toolbar3'].click()
            time.sleep(1)

            send_keys(PIC_PATH)
            time.sleep(2)
            send_keys('{VK_RETURN}')
            time.sleep(3)

            send_keys("%s")  # alt+s to save
            time.sleep(2)
            try:
                confirm_dialog = app['确认另存为']
                confirm_dialog['否(&N)'].click()
                send_keys('{VK_ESCAPE}')
                time.sleep(2)
                send_keys('{VK_ESCAPE}')
            except pywinauto.findbestmatch.MatchError:
                pass

            # RETURN TO PAGE
            # actions = ActionChains(driver)
            # actions.move_to_element(zoomed_img)
            # actions.click(zoomed_img)
            time.sleep(1)
            
            count += 1          
        except IndexError:
            print("OUT OF RANGE. NOW LOADING...")
            send_keys(Keys.PAGE_DOWN)

if __name__ == '__main__':
    driver = prepare_driver("https://www.tumblr.com/login")

    reset(driver)
    find_pics(driver)

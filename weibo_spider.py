import time

import selenium
from pywinauto.keyboard import send_keys
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from utils import prepare_driver, save_pics

PIC_PATH = r"F:\weibo_pages"


def reset(driver, album_page, username, password):
    # driver.switch_to.window(weibo_page)
    # driver.refresh()

    time.sleep(60)
    input_account = driver.find_element(By.XPATH, '//input[@id="loginname"]')
    input_psw = driver.find_element(By.XPATH, '//input[@type="password"]')
    input_account.send_keys(username)
    input_psw.send_keys(password)
    button_login = driver.find_elements(By.XPATH, '//a[@action-type="btn_submit"]')[0]
    button_login.click()  # 点击登录

    time.sleep(5)
    # 手动刷新
    driver.refresh()
    time.sleep(10)
    driver.get(album_page)
    time.sleep(20)


def navigate(driver):
    count = 0
    while True:
        imgs = driver.find_elements(By.XPATH, '//div[contains(text(),"全部图片")]/../..//img')
        print(len(imgs))
        try:
            img_tag = imgs[count]
            print("ZOOM IN")
            zoomed = click_to_zoom(driver, img_tag)

            time.sleep(2)
            print("OPEN ORIGINAL")
            original_ = open_original_page(driver, zoomed)
            time.sleep(1)
            # 按时间顺序排列
            print("SAVE")
            save_pics(driver, original_, PIC_PATH, save_file_name=str(10000000000-round(time.time())))
            time.sleep(2)

            print("CLOSE ORIGINAL")
            close_original_page(driver)
            time.sleep(1)

            print("ZOOM OUT")
            return_from_zoom(driver)
            time.sleep(2)
            count += 1

        except IndexError:
            print("OUT OF RANGE. NOW LOADING...")
            send_keys(Keys.PAGE_DOWN)


def click_to_zoom(driver, img):
    actions = ActionChains(driver)
    actions.move_to_element(img)
    actions.click(img)
    actions.perform()

    time.sleep(10)  # 等待加载

    return driver.find_elements(By.XPATH, '//div[@align="center"]//img')[0]


def open_original_page(driver, img_tag):
    actions = ActionChains(driver)
    actions.move_to_element(img_tag)
    actions.perform()
    time.sleep(1)
    original_button = driver.find_element(By.XPATH, '//span[text()="原图"]')
    original_button.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    return driver.find_element(By.XPATH, '//img')
    # actions.move_to_element(original_button)


def close_original_page(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    driver.close()
    driver.switch_to.window(handles[0])


def return_from_zoom(driver):
    try:
        driver.find_element(By.XPATH, '//div[@title="关闭弹层"]').click()
    except selenium.common.exceptions.ElementNotInteractableException:
        print("已关闭放大")
        pass


if __name__ == '__main__':
    username = ''
    password = ""
    driver = prepare_driver("https://weibo.com/login.php")
    reset(driver, "https://weibo.com/u/3982248071?tabtype=album", username, password)
    navigate(driver)
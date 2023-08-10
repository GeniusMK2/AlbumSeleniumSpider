# import datetime
import time
from datetime import datetime

import selenium
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from utils import save_pics, prepare_driver

PIC_PATH = r"F:\twitter_images"

already_visited = set()


def reset(driver, album_page, username, password):
    # 等待加载
    time.sleep(40)
    # driver.get("https://twitter.com/i/flow/login")
    username_input = driver.find_element(By.XPATH, '//input[@type="text"]')
    username_input.send_keys(username)
    time.sleep(2)
    next_button = driver.find_element(By.XPATH, '//span[text()="下一步"]/../..')
    next_button.click()
    time.sleep(5)

    if len(driver.find_elements(By.XPATH, '//span[contains(text(), "异常登录")]')) > 0:
        account_name = "GeniusMK2"
        driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]').send_keys(account_name)
        time.sleep(2)
        next_button = driver.find_element(By.XPATH, '//span[text()="下一步"]/../..')
        next_button.click()
        time.sleep(5)

    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(password)
    time.sleep(2)
    try:
        next_button = driver.find_elements(By.XPATH, '//span[text()="登录"]/../..')[1]
    except IndexError:
        next_button = driver.find_element(By.XPATH, '//span[text()="登录"]/../..')
    next_button.click()
    time.sleep(20)
    driver.get(album_page)
    time.sleep(30)


def click_to_zoom(driver, img_tag):
    actions = ActionChains(driver)
    actions.move_to_element(img_tag)
    actions.click(img_tag)
    actions.perform()
    time.sleep(5)  # 等待加载


def return_from_zoom(driver):
    try:
        driver.find_element(By.XPATH, '//div[@aria-label="关闭"]').click()
    except ElementNotInteractableException:
        print("已关闭放大")
        pass


def navigate(driver):
    # 这个和微博tag一样会删掉一部分。所以需要根据时间线确认（同一个人同一时间只有一条推）
    while True:
        twitter_tags = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
        print(len(twitter_tags))
        try:
            for current_tag in twitter_tags:
                # 鉴定是否已经遍历
                t_ = check_if_visited(current_tag)  # 推测可能是因为pgdn之后，tag位置发生了变动
                if t_ is not None:
                    # print(current_tag)
                    if navigate_respectively(driver, current_tag):
                        already_visited.add(t_)
        except selenium.common.exceptions.WebDriverException:
            print("FOR BREAK")
            pass
        # for遍历后直接接pgdn

        print('pgdn')
        driver.find_element(By.XPATH, '//body').send_keys(Keys.DOWN)


def navigate_respectively(driver, tweet_tag):
    try:
        # 点开第一张图然后一路按next直到没有
        first_img = tweet_tag.find_element(By.XPATH, './/img[@alt="图像"]')
        click_to_zoom(driver, first_img)
        count = 0
        while count < 4:  # 最多4张图
            # 每次都要重新读取
            img_tags = driver.find_elements(By.XPATH, '//div[@data-testid="swipe-to-dismiss"]//img')
            img_tag = img_tags[count]
            print(count)
            if not save_pics(driver, img_tag, PIC_PATH, ):
                return False
            try:
                actions = ActionChains(driver)
                actions.move_to_element(img_tag)
                actions.perform()
                time.sleep(1)
                next_button = driver.find_element(By.XPATH, '//div[@aria-label="下一张幻灯片"]')
                next_button.click()
                time.sleep(5)
                count += 1
            except NoSuchElementException:
                close_button = driver.find_element(By.XPATH, '//div[@aria-label="关闭"]')
                close_button.click()
                time.sleep(5)
                break
        return True
    except NoSuchElementException:
        # TODO 尝试扒m3u8或至少获取链接
        print("这条推特没有图片")
        return True


def check_if_visited(tag):
        t_ = tag.find_element(By.XPATH, ".//time/..").get_attribute("href")
        print(t_)
        # timestamp = datetime.strptime(t_, "%Y-%m-%dT%H:%M:%S.000Z")
        if t_ in already_visited:
            return None
        # already_visited.add(t_)
        return t_


if __name__ == '__main__':
    username = ''
    password = ""
    driver = prepare_driver("https://twitter.com/i/flow/login")
    reset(driver, "https://twitter.com/GeniusMK2/media", username, password)
    navigate(driver)

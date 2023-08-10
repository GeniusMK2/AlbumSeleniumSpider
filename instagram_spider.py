from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

from utils import prepare_driver, save_pics

PIC_PATH = "F:/instagram_images"

already_ = set()


def reset(driver, album_page, username, password):
    # driver.switch_to.window("https://www.instagram.com/")
    sleep(30)
    input_username = driver.find_element(By.XPATH, '//input[@name="username"]')
    input_username.send_keys(username)
    sleep(1)
    input_password = driver.find_element(By.XPATH, '//input[@name="password"]')
    input_password.send_keys(password)
    sleep(1)
    login_button = driver.find_element(By.XPATH, '//div[text()="登录"]/..')
    login_button.click()
    sleep(15)
    try:
        later_button = driver.find_element(By.XPATH, '//div[text()="以后再说"]')
        later_button.click()
    except:
        print("请手动点击取消cookie")
    sleep(10)
    try:
        # 此处需要点击取消通知
        later_button = driver.find_element(By.XPATH, '//button[text()="以后再说"]')
        later_button.click()
    except:
        print("请手动点击取消通知")
    sleep(10)
    driver.get(album_page)
    sleep(30)


def zoom_in(img_tag):
    actions = ActionChains(driver)
    actions.move_to_element(img_tag)
    actions.click(img_tag)
    actions.perform()
    sleep(5)  # 等待加载


def zoom_out(driver):
    driver.find_element(By.XPATH, "//body").click()
    # pass


def navigate(driver):
    while True:
        img_tags = driver.find_elements(By.XPATH, '//article//img')
        for img_tag in img_tags:
            try:
                src = img_tag.get_attribute("src")
                sleep(1)
                print(src)
                file_name = src.split('?')[0].split('/')[-1]
                if file_name not in already_:
                    driver.switch_to.new_window('tab')
                    driver.get(src)
                    sleep(10)
                    img = driver.find_element(By.XPATH, "//img")
                    save_pics(driver, img, PIC_PATH)
                    sleep(2)
                    driver.close()
                    sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    already_.add(file_name)
            except StaleElementReferenceException:
                # 试试这样？
                driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_UP)
                break

            # zoom_out(driver)
        driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)


if __name__ == '__main__':
    username = ''
    password = ""
    driver = prepare_driver("https://www.instagram.com/")
    reset(driver, "https://www.instagram.com/hirogatoinc/", username, password)
    navigate(driver)
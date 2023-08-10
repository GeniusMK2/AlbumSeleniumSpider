import time

from pywinauto.keyboard import send_keys
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils import save_pics, prepare_driver

# from selenium.webdriver.common.service import Service

base_path = "./images"

PIC_PATH = r"F:\tumblr_images"
COUNT = 0


def reset(driver, homepage, username, password):
    email_input = driver.find_element(By.XPATH, '//input[@name="email"]')
    email_input.send_keys()
    time.sleep(2)
    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys("A1829643210a")
    time.sleep(2)
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()
    time.sleep(5)
    driver.get(homepage)
    time.sleep(10)
    continue_button = driver.find_element(By.XPATH, '//button[text()="ブログを表示"]')
    continue_button.click()
    # Wait for page loading complete
    time.sleep(30)


def find_pics(driver):
    global COUNT
    while True:
        imgs = driver.find_elements(By.XPATH, '//div[@data-testid]//button/span/figure/div/img')
        print(len(imgs))
        try:
            # TOMORROW TO BE CONTINUED
            if COUNT > 250:
                break

            img = imgs[COUNT]
            # ZOOMED
            # actions.move_to_element(img)
            # actions.context_click(img)
            # actions.click(img)
            # actions.perform()
            # time.sleep(2)
            # actions = ActionChains(driver)
            # zoomed_img = driver.find_elements(By.XPATH, '//button[@aria-label="画像を閉じる"]/span/img')

            save_pics(driver, img, PIC_PATH)

            # RETURN TO PAGE
            # actions = ActionChains(img)
            # actions.move_to_element(img)
            # actions.click(img)

            COUNT += 1
        except IndexError:
            print("OUT OF RANGE. NOW LOADING...")
            send_keys(Keys.PAGE_DOWN)


if __name__ == '__main__':
    username = ''
    password = ""
    driver = prepare_driver("https://www.tumblr.com/login")
    reset(driver, "https://www.tumblr.com/badrachel?redirect_to=%2Fbadrachel&source=content_warning_wall",
          username, password)
    find_pics(driver)

import time

from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from utils import save_pics, prepare_driver

PIC_PATH = "F:/pixiv_images"


def navigate(driver, base_link, total_page=1):
    template = "{base_link}?p={page}"
    for p in range(total_page):
        # https: // www.pixiv.net / users / 73809003 / artworks?p = 3
        driver.get(template.format(base_link, p))
        time.sleep(2)
        img_a_tags = driver.find_elements(By.XPATH, '//section//img/../..')
        for img_a_tag in img_a_tags:
            href = img_a_tag.get_attribute("href")

            driver.switch_to.new_window('tab')
            driver.get(href)

            inner_count = int(driver.find_elements(By.XPATH, '//div[@aria-label="预览"]/div/span').text[1][1:])
            zoom = driver.find_element(By.XPATH, '//a[@href="/"]/img')
            zoom.click()

            for index in range(inner_count):
                pics_tag = driver.find_elements(By.XPATH, '//div[@role="presentation"]/div/div/div/img')
                save_pics(driver, pics_tag, PIC_PATH)
                driver.find_element(By.XPATH, "//body").send_keys(Keys.DOWN)

            # 这个窗口应该不需要zoom out,可以直接关闭并切换回原窗口的？
            zoom_out = driver.find_element(By.XPATH, '//div[@role="presentation"]//a')
            zoom_out.click()




def reset(driver, album_page, username, password):
    # driver.get("https://accounts.pixiv.net/login")
    username_tag = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
    username_tag.send_keys(username)
    time.sleep(2)
    password_tag = driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
    password_tag.send_keys(password)
    time.sleep(2)
    submit_button = driver.find_element(By.XPATH, '//button[text()="登录"]')
    submit_button.click()
    time.sleep(60)
    # 注意后缀artworks
    # driver.get("https://www.pixiv.net/users/4473989/artworks")
    driver.get(album_page)
    time.sleep(60)


if __name__ == '__main__':
    username = ''
    password = ""
    album_pages = "https://www.pixiv.net/users/4473989/artworks"
    driver = prepare_driver("https://accounts.pixiv.net/login")
    reset(driver, album_pages, username, password)
    navigate(driver, album_pages, total_page=11)

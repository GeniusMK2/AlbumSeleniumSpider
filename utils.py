import time

import pywinauto
import undetected_chromedriver as ucd
from pywinauto.keyboard import send_keys
from selenium.webdriver import ActionChains


def save_pics(driver, img_tag, save_path, save_file_name=""):
    actions = ActionChains(driver)
    actions.move_to_element(img_tag)
    actions.context_click(img_tag)
    actions.perform()
    time.sleep(2)
    send_keys('v')
    # 有时候会按不下去
    # 接下来使用pywinauto操作保存
    time.sleep(2)
    app = pywinauto.Desktop()
    time.sleep(2)
    # 控制台展示全部控件
    # dialog.print_control_identifiers()
    dialog = app['另存为']
    time.sleep(1)
    try:
        dialog['Toolbar4'].click()
        time.sleep(1)
        send_keys(save_path)
        time.sleep(2)
        send_keys('{VK_RETURN}')
        time.sleep(2)
        if len(save_file_name) > 0:
            # print(save_file_name)
            # 此处无效？
            dialog['Edit2'].click()
            dialog['Edit2'].type_keys(save_file_name, with_spaces=False)
            # dialog["保存(&S)"].click()
            time.sleep(2)
        dialog["Button"].click()
        # dialog['保存(&S)Button'].click()  # 这句容易出错
        # send_keys("%s")  # alt+s保存
        time.sleep(2)
    except pywinauto.findbestmatch.MatchError:
        # 如果出错，多按几次esc重置页面
        print("match error1")
        send_keys('{VK_ESCAPE}')
        time.sleep(1)
        send_keys('{VK_ESCAPE}')
        time.sleep(1)
        send_keys('{VK_ESCAPE}')
        time.sleep(1)
        send_keys('{VK_ESCAPE}')
        time.sleep(1)
        # dialog.print_control_identifiers()
        return False
    try:
        confirm_dialog = app['确认另存为']
        # 干脆覆盖了
        confirm_dialog['是(&Y)'].click()
        # confirm_dialog['否(&N)'].click()
        # send_keys('{VK_ESCAPE}')
        # send_keys('{VK_ESCAPE}')
        time.sleep(2)
    except pywinauto.findbestmatch.MatchError:
        pass
    time.sleep(1)
    return True


def prepare_driver(url):
    ret = ucd.Chrome()
    ret.maximize_window()
    ret.get(url)
    return ret

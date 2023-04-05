# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

USER = ...
PASS = ...
RND_STR = 'asdfsadfas'
FOLLOWERS_BOX_XPATH = '''//div/div/div/div[2]/
                         div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/
                         div[2]/div[1]/div'''
FOLLOWERS_XPATH = '''//div/div/div/div[2]/div/div
                     /div[1]/div/div[2]/div/div/div/div
                     /div[2]/div/div/div[2]/div[1]/div/div'''
FOLLOWING_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div
                     /div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div'''
FOLLOWING_BOX_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]
                         /div/div/div/div/div[2]/div/div/div[3]/div[1]'''
USERS_PER_SCREEN = 6

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = webdriver.Safari()
    driver.set_window_position(0, 0)
    driver.set_window_size(830, 825)

    driver.get('http://instagram.com')
    sleep(5)
    inputs = driver.find_elements(by=By.TAG_NAME, value='input')
    inputs[1].click()
    inputs[1].send_keys(RND_STR)
    inputs[0].click()
    inputs[0].clear()
    inputs[0].send_keys(USER)
    inputs[1].click()
    inputs[1].clear()
    inputs[1].send_keys(PASS)

    button = [i for i in driver.find_elements(by=By.TAG_NAME, value='button') if 'Log' in i.text][0]
    button.submit()

    sleep(10)
    button = [i for i in driver.find_elements(by=By.TAG_NAME, value='button') if 'Save' in i.text][0]
    button.click()
    sleep(10)

    # followers
    driver.get(f'http://instagram.com/{USER}/followers')
    sleep(10)
    followers_box = driver.find_element(By.XPATH, FOLLOWERS_BOX_XPATH)
    i = 0
    while True:
        sleep(3)
        try:
            i += USERS_PER_SCREEN
            t = driver.find_element(By.XPATH, FOLLOWERS_XPATH + f'[{i}]')
            driver.execute_script("arguments[0].scrollIntoView();", t)

        except NoSuchElementException:
            print('Followers is over', i)
            break
    followers = [i.get_attribute('href')
                 for i in followers_box.find_elements(By.TAG_NAME, 'a')
                 if i.text != '']
    sleep(5)
    # following
    driver.get(f'http://instagram.com/{USER}/following')
    sleep(10)
    followers_box = driver.find_element(By.XPATH, FOLLOWING_BOX_XPATH)
    i = 0
    while True:
        sleep(3)
        try:
            i += USERS_PER_SCREEN
            t = driver.find_element(By.XPATH, FOLLOWING_XPATH + f'[{i}]')
            driver.execute_script("arguments[0].scrollIntoView();", t)
        except NoSuchElementException:
            print('Following is over', i)
            break

    following = [i.get_attribute('href')
                 for i in followers_box.find_elements(By.TAG_NAME, 'a')
                 if i.text != '']
    driver.close()
    print(set(following) - set(followers))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

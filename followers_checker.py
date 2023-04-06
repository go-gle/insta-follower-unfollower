from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from constants import LONG_SLEEP, SHORT_SLEEP, WINDOW_SIZE, RND_STR
from random import random


class FollowerChecker:
    def __init__(self: 'FollowerChecker',
                 login: str,
                 password: str,
                 ) -> None:
        self.login = login
        self.password = password
        self._init_insta()

    # Yep, sleeps are dump :/
    @staticmethod
    def _random_sleep(min_sleep: float, max_sleep: float) -> None:
        delta = max_sleep - min_sleep
        sleep(min_sleep + random() * delta)

    def _init_insta(self: 'FollowerChecker') -> None:
        self.driver = webdriver.Safari()
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(*WINDOW_SIZE)
        self.driver.get('http://instagram.com')
        sleep(LONG_SLEEP)

    def _login(self: 'FollowerChecker') -> None:
        inputs = self.driver.find_elements(by=By.TAG_NAME, value='input')
        login_input, pass_input = inputs[0], inputs[1]
        pass_input.click()
        # idk why but had a problem with focus when 'SHOW' appears in pass input
        pass_input.send_keys(RND_STR)
        login_input.click()
        login_input.clear()
        login_input.send_keys(self.login)
        pass_input.click()
        pass_input.clear()
        pass_input.send_keys(self.password)
        login_button = [i for i in self.driver.find_elements(by=By.TAG_NAME, value='button')
                        if 'Log' in i.text or 'Войти' in i.text][0]
        login_button.submit()

        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        save_button = [i for i in self.driver.find_elements(by=By.TAG_NAME, value='button')
                       if 'Save' in i.text or 'Сохранить' in i.text][0]
        save_button.click()
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)

    def _scroll_users(self: 'FollowerChecker', users_container: WebElement) -> None:
        t = None
        t1 = users_container.find_elements(By.XPATH, './div/div/div/*')[-1]
        while t1 != t:
            t = t1
            self.driver.execute_script("arguments[0].scrollIntoView();", t1)
            self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
            t1 = users_container.find_elements(By.XPATH, './div/div/div/*')[-1]

    def get_followers(self: 'FollowerChecker') -> list:
        self.driver.get(f'http://instagram.com/{self.login}/followers')
        followers = self.get_users(following_flag=False)
        print(f'Total # followers is {len(followers)}')
        return followers

    def get_users(self: 'FollowerChecker', following_flag: bool) -> list:
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        if following_flag:
            divs = [i for i in self.driver.find_elements(By.TAG_NAME, 'div')
                    if i.text == 'Following' or i.text == 'Ваши подписки']
        else:
            divs = [i for i in self.driver.find_elements(By.TAG_NAME, 'div')
                    if i.text == 'Followers' or i.text == 'Подписчики']
        users_header = divs[0]
        user_box = users_header.find_element(By.XPATH, '../../../../*')
        self._scroll_users(user_box)
        users = [i.get_attribute('href')
                 for i in user_box.find_elements(By.TAG_NAME, 'a')
                 if i.text != '']
        return users

    def get_following(self: 'FollowerChecker') -> list:
        self.driver.get(f'http://instagram.com/{self.login}/following')
        following = self.get_users(following_flag=True)
        print(f'Total # following is {len(following)}')
        return following

    def get_followers_unfollowers(self: 'FollowerChecker') -> list:
        self._login()
        return list(set(self.get_following()) - set(self.get_followers()))

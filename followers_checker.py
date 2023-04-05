from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from constants import *
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

        login_button = [i for i in self.driver.find_elements(by=By.TAG_NAME, value='button') if 'Log' in i.text][0]
        login_button.submit()

        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        save_button = [i for i in self.driver.find_elements(by=By.TAG_NAME, value='button') if 'Save' in i.text][0]
        save_button.click()
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)

    def _get_list(self: 'FollowerChecker',
                  followers_box_path: str,
                  followers_path: str,
                  ) -> list:
        followers_box = self.driver.find_element(By.XPATH, followers_box_path)
        i = 0
        while True:
            self._random_sleep(SHORT_SLEEP, 1.5 * SHORT_SLEEP)
            try:
                i += USERS_PER_SCREEN
                t = self.driver.find_element(By.XPATH, followers_path + f'[{i}]')
                self.driver.execute_script("arguments[0].scrollIntoView();", t)
            except NoSuchElementException:
                break
        user_list = [i.get_attribute('href')
                     for i in followers_box.find_elements(By.TAG_NAME, 'a')
                     if i.text != '']
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        return user_list

    def get_followers(self: 'FollowerChecker') -> list:
        self.driver.get(f'http://instagram.com/{self.login}/followers')
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        followers = self._get_list(FOLLOWERS_BOX_XPATH, FOLLOWERS_XPATH)
        print(f'Total # unfollowing is {len(followers)}')
        return followers

    def get_following(self: 'FollowerChecker') -> list:
        self.driver.get(f'http://instagram.com/{self.login}/following')
        self._random_sleep(LONG_SLEEP, 1.5 * LONG_SLEEP)
        following = self._get_list(FOLLOWING_BOX_XPATH, FOLLOWING_XPATH)
        print(f'Total # following  is {len(following)}')
        return following

    def get_followers_unfollowers(self: 'FollowerChecker') -> list:
        self._login()
        return list(set(self.get_following()) - set(self.get_followers()))

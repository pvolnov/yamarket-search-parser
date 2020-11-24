import json
import re
import time
import traceback
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup
from peewee import fn
from playhouse.shortcuts import model_to_dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import configs
from parser.Models import SearchResult


class Parser(Process):
    """Потоковый парсер ЯМаркета"""

    def __init__(self, i):
        """Инициализация потока"""
        super().__init__()
        self.num = i

    def get_captcha_ans(self, filename):
        with open(filename, "rb") as f:
            task_id = requests.post("https://rucaptcha.com/in.php",
                                    data={
                                        "key": configs.RU_CAPTCHA_APY_KEY
                                    }, files={"file": f}
                                    ).text[3:]

        print(f"Get captcha ID {task_id}")
        captcha_text = ""
        while "OK" not in captcha_text:
            time.sleep(3)
            captcha_text = requests.get("https://rucaptcha.com/res.php",
                                        params={
                                            "key": configs.RU_CAPTCHA_APY_KEY,
                                            "action": "get",
                                            "id": task_id
                                        }).text
            if captcha_text == "ERROR_CAPTCHA_UNSOLVABLE":
                return False, task_id

        captcha_text = captcha_text[3:]
        print(f"Get captcha {task_id} result: {captcha_text}")
        return captcha_text, task_id

    def pass_captcha(self):
        if "captcha" in self.driver.page_source:
            print("Find captcha")
            self.driver.find_element_by_tag_name("img").screenshot(f"captcha_{self.num}.png")

            captcha_text, task_id = self.get_captcha_ans(f"captcha_{self.num}.png")
            if not captcha_text:
                return self.pass_captcha()

            self.driver.find_element_by_class_name("input-wrapper__content").send_keys(captcha_text)
            self.driver.find_element_by_class_name("submit").click()
            time.sleep(2)
            if "captcha" in self.driver.page_source:
                r = requests.get("https://rucaptcha.com/res.php",
                                 params={
                                     "key": configs.RU_CAPTCHA_APY_KEY,
                                     "action": "reportbad",
                                     "id": task_id
                                 })

                print(f"recaptcha {task_id} is incorrect {self.num}:", r.text)
                self.driver.refresh()
                time.sleep(2)
                self.pass_captcha()
            return True
        return False

    def get_params(self, url):
        self.driver.get(url + "/spec")
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html5lib')

        params = {}
        for div in soup.find("div", {"data-apiary-widget-id": "/content/productSpecs"}).div.div.find_all("div"):
            if len(div.find_all("dl")) > 0:
                for dl in div.find_all("dl"):
                    params[dl.dt.span.text] = dl.dd.text
        path = []
        for div in soup.find_all("a", {"itemprop": "item", "title": True}):
            path.append(div["title"])

        if len(path) > 1:
            params["brend"] = path[-1]
            params["category"] = path[-2]

        if len(params) == 0:
            raise Exception("No params found")
        return params

    @staticmethod
    def clear_name(name):

        NUM = r"\d+[,\.]?\d*"

        def to_float(string):
            return float(re.search(NUM, string).group(0).replace(",", "."))

        data = []
        p = re.search(f"{NUM}\s*кг", name)
        if p:
            data.append(to_float(p.group(0)) * 1000)
            name = name.replace(p.group(0), "")

        p = re.search(f"{NUM}\s*г", name)
        if p:
            data.append(to_float(p.group(0)))
            name = name.replace(p.group(0), "")

        p = re.search(f"{NUM}\s*%", name)
        if p:
            data.append(to_float(p.group(0)))
            name = name.replace(p.group(0), "")

        name = re.sub(r"[^а-яa-z\-]", " ", name.lower())
        name = re.sub(r"\s+", " ", name.lower())
        return data, name

    def get_options(self, name: str) -> list:
        self.driver.get("https://market.yandex.ru/")
        time.sleep(0.5)
        self.driver.find_element_by_id("header-search").send_keys(name, Keys.ENTER)
        res = []

        for i in range(5):
            time.sleep(1)
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html5lib')
            for a in soup.find_all("article"):
                url = a.find("a", {"href": lambda x: x and "product" in x})
                if url:
                    res.append({
                        "name": a.find("a", {"title": True})["title"],
                        "url": "https://market.yandex.ru" +
                               url["href"].split("?")[0],
                        "price": a.find("span", {"data-autotest-currency": "₽"})["data-autotest-value"] if a.find(
                            "span", {
                                "data-autotest-currency": "₽"}) else 0
                    })
            if res: return res[:6]

        raise Exception("Result not found")

    def run(self):
        """Запуск потока"""
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(options=chrome_options)
        # from webdriver_manager.chrome import ChromeDriverManager
        #
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # time.sleep(self.num * 3)

        self.driver = webdriver.Remote(
            command_executor=configs.SELENOID_ADRESS,
            desired_capabilities={
                "browserName": "chrome",
                "sessionTimeout": "1m"
            },
        )

        print(f"Thread {self.num} is runing")

        while True:
            try:
                tasks = SearchResult.select().where(SearchResult.done == False).limit(100).order_by(
                    fn.random()).execute()
                for task in tasks:

                    try:
                        start_time = time.time()
                        options = self.get_options(task.orig_name)
                        for o in options[:3]:
                            o["specifications"] = self.get_params(o["url"])

                        task.options = options
                        task.name = options[0]["name"]
                        task.url = options[0]["url"]
                        task.specifications = options[0]["specifications"]
                        if task.url != "":
                            task.done = True
                        task.save()

                        dt = start_time - time.time()
                        print(f"Th-{self.num}:: Item complete: {task.orig_name} - {dt}, {len(options)} cards")

                    except Exception as e:
                        traceback.print_exc()
                        print(task.orig_name)
                        if not self.pass_captcha():
                            print("Empty Result")
                            SearchResult.set_by_id(task.id, {"done": True})

                if len(tasks) < 100:
                    time.sleep(3600)
            except Exception as e:
                print(e)
                break

        self.driver.quit()

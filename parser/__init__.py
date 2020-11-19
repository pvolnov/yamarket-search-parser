import pickle
from multiprocessing import Queue

from parser.Parser import Parser


def parse(urls, proxies, visibility=False):
    """
    Запускаем программу
    """
    queue = Queue()

    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        queue.put(url)

    with open("cookies.pickle", "rb") as f:
        cookies = pickle.load(f)

    # Запускаем потом и очередь
    threads = []
    for i in range(len(proxies)):
        t = Parser(queue, i, cookies, proxies[i], visibility=visibility)
        t.start()
        threads.append(t)

    # Ждем завершения работы очереди
    for t in threads:
        t.join()

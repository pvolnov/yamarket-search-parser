import time

from parser import Parser

if __name__ == "__main__":

    # Запускаем потом и очередь
    threads = []
    while True:
        alive = 0
        for t in threads:
            # t.join(timeout=0)
            if t.is_alive():
                alive += 1

        while alive < 3:
            alive += 1
            t = Parser(alive)
            t.start()
            threads.append(t)
            print("Total threads:", len(threads))

        time.sleep(5)

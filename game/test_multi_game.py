import pygame as pg
import multiprocessing


class MultiTest:
    def __init__(self):
        pass

    def screen1_show(self):
        pg.display.init()
        self.screen1 = pg.display.set_mode((640, 480))
        self.screen1.fill((255, 0, 255))
        pg.display.update()

    def screen2_show(self):
        pg.display.init()
        self.screen2 = pg.display.set_mode((480, 640))
        self.screen2.fill((0, 255, 0))
        pg.display.update()

    def multi_process(self):
        a = multiprocessing.Process(self.screen1_show())
        b = multiprocessing.Process(self.screen2_show())
        a.start()
        b.start()

    def run(self):
        while True:
            self.multi_process()


if __name__ == '__main__':
    pg.init()
    test = MultiTest()
    test.run()
    pg.quit()

import os
import threading
import time
from typing import IO
import cjen

from cjen.dada.smile import SmileVoice


test_data = {"log1.log": list(range(1, 20)),
             "log2.log": list(range(21, 40)),
             "log3.log": list(range(41, 60)),
             "log4.log": list(range(61, 80)),
             "log5.log": list(range(81, 100))}


def setup_function():
    for log_file in list(test_data.keys()):
        if os.path.exists(log_file): os.remove(log_file)


@cjen.haha(LogPath=os.path.curdir, LogName=list(test_data.keys())[0], Mode='a')
def logs1(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


@cjen.haha(LogPath=os.path.curdir, LogName=list(test_data.keys())[1], Mode='a')
def logs2(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


@cjen.haha(LogPath=os.path.curdir, LogName=list(test_data.keys())[2], Mode='a')
def logs3(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


@cjen.haha(LogPath=os.path.curdir, LogName=list(test_data.keys())[3], Mode='a')
def logs4(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


@cjen.haha(LogPath=os.path.curdir, LogName=list(test_data.keys())[4], Mode='a')
def logs5(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


def thread_log(log, values: list[int]):
    for i in values: log(dict(number=i))


def test_smile_parallel1():
    """
    测试 多线程写入不同的文件
    :return:
    """
    for i, log in enumerate([logs1, logs2, logs3, logs4, logs5]):
        t = threading.Thread(target=thread_log, args=(log, list(test_data.values())[i]))
        t.start()
        t.join()
    while len(list(filter(lambda thd: thd.name == SmileVoice.ThreadName and not thd.queue.empty(),
                          threading.enumerate()))) != 0:
        time.sleep(1)

    for log in list(test_data.keys()):
        with open(os.path.join(os.path.curdir, log), 'r') as f:
            numbers = [int(number.rstrip()) for number in f.readlines()]
            assert test_data.get(log) == numbers

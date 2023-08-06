import os
from typing import IO

import cjen


@cjen.haha(LogPath=os.path.curdir, LogName="test_delay.log", Mode='a')
def logs(msg: dict, io: IO):
    io.write("{number}\n".format(**msg))


def test_delay():
    for i in range(10):
        logs(dict(number=i))

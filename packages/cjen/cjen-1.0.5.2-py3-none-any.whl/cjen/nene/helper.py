import os


class FileHelper(object):

    @classmethod
    def read(cls, *path):
        with open(os.path.join(*path), 'r') as f:
            return f.read()

    @classmethod
    def cur_read(cls, *, cur, file):
        """
        与期望文件文件同一路径文件
        :param cur: 文件的__file__参数
        :param file: 文件名
        :return:
        """
        return cls.read(os.path.dirname(cur), file)

    @classmethod
    def replace(cls, rep: dict, *path):
        with open(os.path.join(*path), 'r') as f:
            return f.read().format(**rep)

    @classmethod
    def readlines_str(cls, *path):
        with open(os.path.join(*path), 'r') as f:
            return [line.rstrip() for line in f.readlines()]

    @classmethod
    def readlines_int(cls, path: str):
        with open(path, 'r') as f:
            return [int(line.rstrip()) for line in f.readlines()]

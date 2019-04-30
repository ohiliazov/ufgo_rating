import re
from collections import defaultdict
import pandas as pd
from abc import abstractmethod

df = pd.read_csv('tourneys/T190420D.txt', sep='\s{1,}', header=None, skiprows=10, engine='python')

RESULT_REGEX = re.compile(r'(?P<opponent>\d+)(?P<result>[+\-])(?P<technical>!)?(?:/[wb]\d)?')


class BaseParser:
    RESULT_REGEX = NotImplemented
    SKIP_REGEX = NotImplemented

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.players = {}
        self.data = defaultdict(list)

    @abstractmethod
    def parse(self):
        raise NotImplementedError


class EGFParser(BaseParser):
    RESULT_REGEX = re.compile(r'(?P<opponent>\d+)(?P<result>[+\-])(?P<technical>!)?(?:/[wb]\d)?')
    SKIP_REGEX = re.compile(r'0=')

    def __init__(self, filepath: str):
        super().__init__(filepath)

    def parse(self):
        data = pd.read_csv(self.filepath, sep=r'\s{1,}', header=None, skiprows=10, engine='python')
        for row in data.get_values():
            pin = row[-1]
            key = row[0]
            self.players[key] = pin.lstrip('|')
            for result in row[10:15]:
                if self.SKIP_REGEX.match(result):
                    self.data[key].append((None, None))
                    continue

                opponent, result, technical = RESULT_REGEX.match(result).groups()
                if technical:
                    self.data[key].append((opponent, None))
                else:
                    self.data[key].append((int(opponent), 1 if result == '+' else 0))

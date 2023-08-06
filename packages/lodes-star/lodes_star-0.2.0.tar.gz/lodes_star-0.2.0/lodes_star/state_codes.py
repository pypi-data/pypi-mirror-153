import csv
import os


class Geographies:
    with open(os.path.join(os.path.dirname(__file__), 'geographies.csv')) as csvfile:
        next(csvfile)
        csv_reader = csv.reader(csvfile)
        geographies = dict(csv_reader)

    @classmethod
    def list(cls):
        whitespace = max([len(x) for x in cls.geographies.keys()])
        for k, v in cls.geographies.items():
            print(k, ' '*(whitespace - len(k)), v)
        return

    def __new__(cls, geography=None):
        if geography in cls.geographies.keys():
            return cls.geographies[geography]
        else:
            print("Geography not found")


class State:
    with open(os.path.join(os.path.dirname(__file__), 'states.csv')) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        states = list(csv_reader)

    abb2code = {x['abb']: x['code'] for x in states}
    code2abb = {v: k for k, v in abb2code.items()}

    name2code = {x['name']: x['code'] for x in states}
    code2name = {v: k for k, v in name2code.items()}

    name2abb = {x['name']: x['abb'] for x in states}
    abb2name = {v: k for k, v in name2abb.items()}

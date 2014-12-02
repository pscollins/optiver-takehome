import csv
import abc

from sys import argv
from operator import attrgetter
from collections import namedtuple

BAKE_TIMES = {
    '0': 60,
    '1': 15
}

OVEN_COUNT = 3

class Clock:
    def __init__(self):
        self.time = 0

class Oven:
    def __init__(self, clock):
        self.cooking = None
        self.finishing_at = 0
        self.clock = clock

    def retrieve(self):
        assert(self.cooking is not None)

        self.clock.time = self.finishing_at

        finished = BakedPizza(self.cooking.num,
                              self.cooking.placed_at,
                              self.finishing_at - self.cooking.placed_at)
        self.cooking = None

    def submit(self, pizza):
        self.cooking = pizza
        self.finishing_at = self.clock.time + pizza.bake_time

    def bake(self, pizza):
        finished = self.retrieve()
        self.submit(pizza)
        return finished

class Ovens:
    def __init__(self, ovens):
        self.ovens = ovens
        self.baked_pizzas = []

    def next_available(self):
        return min(self.ovens, key=attrgetter("finishing_at"))

    def bake(self, pizza):
        finished = self.next_available().bake(pizza)
        if finished is not None:
            self.baked_pizzas.append(finished)

UnbakedPizza = namedtuple("Pizza", ["placed_at", "num", "bake_time"])
BakedPizza = namedtuple("BakedPizza", ["num", "placed_at", "finished_at"])

def parse(infile):
    '''Given a file handle corresponding to the input CSV, construct a
list of Pizza objects.'''

    reader = csv.reader(infile)

    pizzas = [Pizza(placed_at, num, BAKE_TIMES[ty])
              for placed_at, num, ty in reader]

    return pizzas

def write(pizzas, outfile):
    '''Given a list of Pizza objects, compute their finished times and
write them out to the result file.'''

    writer = csv.writer(outfile)
    clock = Clock()
    ovens = Ovens(Oven(clock) for _ in range(OVEN_COUNT))

    for pizza in pizzas:
        ovens.bake(pizza)

    writer.writerows(ovens.flush())


def main(infile, outfile):
    pizzas = parse(infile)
    write(pizzas, outfile)


if __name__ == "__main__":
    main(open(argv[1]), open(argv[2], "w"))

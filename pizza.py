import csv
import abc

from sys import argv
from operator import attrgetter

class ComparableMixin:
    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and self.__dict__ == obj.__dict__


class Clock(ComparableMixin):
    '''A wraper around a mutable integer to keep track of the current time.'''

    def __init__(self):
        self.time = 0

    def advance(self, pizza):
        '''Advance the time by the correct amount to complete baking a pizza
and return the new current time.'''
        # Make sure we don't bake pizzas from the future
        # self.time = max(self.time, pizza.placed_at)
        # self.time += pizza.bake_time
        self.time = pizza.finished_at
        return self.time

class Ovens(ComparableMixin):
    OVEN_COUNT = 3

    def __init__(self, clock):
        self._orders = []
        self._results = []
        self._clock = clock

    def _pop_next(self):
        # This is O(n), but we can't do any better with an array
        # to_bake = min(self._orders, key=attrgetter("bake_time"))
        to_bake = min(self._orders, key=attrgetter("finished_at"))
        self._clock.advance(to_bake)
        self._results.append(to_bake.bake(self._clock))
        self._orders.remove(to_bake)

    def submit(self, pizza):
        if len(self._orders) > self.OVEN_COUNT:
            self._pop_next()

        pizza.bake(self._clock)
        self._orders.append(pizza)



    def flush(self):
        while self._orders:
            self._pop_next()

        return self._results

class AbstractPizza(ComparableMixin, metaclass=abc.ABCMeta):
    '''The abstract base class for our two concrete pizza types.'''

    def __init__(self, placed_at, num):
        self.placed_at = int(placed_at)
        self.num = int(num)
        self.finished_at = None

    def bake(self, clock):
        '''Increment the system clock, set the finished time of the pizza, and
return a the result to be written out to the result file.'''

        # Only bake once
        if self.finished_at is None:
            self.finished_at = max(clock.time, self.placed_at) + self.bake_time

        return self._result()

    def _result(self):
        return (self.num, self.finished_at, self.finished_at - self.placed_at)


class DeepDishPizza(AbstractPizza):
    def __init__(self, placed_at, num):
        super().__init__(placed_at, num)
        self.bake_time = 60

class ThinCrustPizza(AbstractPizza):
    def __init__(self, placed_at, num):
        super().__init__(placed_at, num)
        self.bake_time = 15

def parse(infile):
    '''Given a file handle corresponding to the input CSV, construct a
list of Pizza objects.'''

    clock = Clock()
    reader = csv.reader(infile)

    cons = {
        '0': lambda placed_at, num: DeepDishPizza(placed_at, num),
        '1': lambda placed_at, num: ThinCrustPizza(placed_at, num)
    }


    pizzas = [cons[ty](placed_at, num) for placed_at, num, ty in reader]

    return pizzas

def write(pizzas, outfile):
    '''Given a list of Pizza objects, compute their finished times and
write them out to the result file.'''

    writer = csv.writer(outfile)
    ovens = Ovens(Clock())

    for pizza in pizzas:
        ovens.submit(pizza)

    writer.writerows(ovens.flush())


def main(infile, outfile):
    pizzas = parse(infile)
    write(pizzas, outfile)


if __name__ == "__main__":
    main(open(argv[1]), open(argv[2], "w"))

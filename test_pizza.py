import unittest
from unittest import mock

from pizza import Clock, UnbakedPizza, parse, write

@unittest.skip
class TestClock(unittest.TestCase):
    def test_advance(self):
        clock = Clock()
        deep_pizza = DeepDishPizza(0, 1)
        thin_pizza = ThinCrustPizza(0, 1)
        future_pizza = DeepDishPizza(120, 1)

        clock.advance(deep_pizza)
        self.assertEqual(clock.time, 60)
        clock.advance(thin_pizza)
        self.assertEqual(clock.time, 75)
        clock.advance(future_pizza)
        self.assertEqual(clock.time, 180)

        self.assertEqual(clock.advance(thin_pizza), 195)

@unittest.skip
class TestPizza(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()

    def test_deep(self):
        pizza = DeepDishPizza(0, 1)
        self.assertEqual(pizza.bake(self.clock),
                         (1, 60, 60))

    def test_thin(self):
        pizza = ThinCrustPizza(0, 1)
        self.assertEqual(pizza.bake(self.clock),
                         (1, 15, 15))

    def test_deep_thin(self):
        deep = DeepDishPizza(0, 1)
        thin = ThinCrustPizza(0, 2)

        self.assertEqual(deep.bake(self.clock),
                         (1, 60, 60))
        self.assertEqual(thin.bake(self.clock),
                         (2, 75, 75))

    def test_thin_deep(self):
        deep = DeepDishPizza(0, 1)
        thin = ThinCrustPizza(0, 2)

        self.assertEqual(thin.bake(self.clock),
                         (2, 15, 15))
        self.assertEqual(deep.bake(self.clock),
                         (1, 75, 75))

    def test_offset(self):
        pizza = DeepDishPizza(14, 1)
        self.assertEqual(pizza.bake(self.clock),
                         (1, 74, 60))

    def test_start(self):
        first = DeepDishPizza(0, 1)
        second = DeepDishPizza(10, 2)

        self.assertEqual(first.bake(self.clock),
                         (1, 60, 60))
        self.assertEqual(second.bake(self.clock),
                         (2, 120, 110))
@unittest.skip
class TestOvens(unittest.TestCase):
    def test_submit_and_flush(self):
        clock = Clock()
        first = None

class TestIO(unittest.TestCase):
    def setUp(self):
        clock = Clock()
        self.pizzas = [
            UnbakedPizza(0, 1, 60),
            UnbakedPizza(0, 2, 15),
            UnbakedPizza(10, 3, 15),
            UnbakedPizza(15, 4, 60)
        ]

    def test_parse(self):
        infile = ["0,1,0", "0,2,1", "10,3,1", "15,4,0"]

        self.assertEqual(parse(infile), self.pizzas)

        # self.assertEqual(actual, self.pizzas)

    def test_write(self):
        outfile = mock.mock_open()()
        write(self.pizzas, outfile)

        outfile.write.assert_has_calls([
            mock.call("2,15,15\r\n"),
            mock.call("3,25,15\r\n"),
            mock.call("1,60,60\r\n"),
            mock.call("4,75,60\r\n")
        ])

if __name__ == "__main__":
    unittest.main()

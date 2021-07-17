import unittest
from src.main.functions.order.create_order import calc_amount


# Class for testing the calculated total amount of an order
class TestCalcAmount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_calc_normal_order(self):
        order_items = [
            {
                'amount': 100
            },
            {
                'amount': 250
            },
            {
                'amount': 1
            }
        ]
        self.assertEqual(calc_amount(order_items), 351)

    def test_calc_all_zeros(self):
        order_items = [
            {
                'amount': 0
            },
            {
                'amount': 0
            },
            {
                'amount': 0
            }
        ]
        self.assertEqual(calc_amount(order_items), 0)


if __name__ == '__main__':
    unittest.main()

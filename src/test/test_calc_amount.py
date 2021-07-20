from unittest import TestCase, mock, main
import os


# Class for testing the calculated total amount of an order
@mock.patch.dict(os.environ, {'FRONTEND_ORIGIN': 'FRONTEND_ORIGIN'})
class TestCalcAmount(TestCase):

    def test_calc_normal_order(self):
        print(os.environ["FRONTEND_ORIGIN"])

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

        # Import is here bc it will throw an error otherwise for not finding the env variables
        from src.main.functions.order.create_order import calc_amount

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
        # Import is here bc it will throw an error otherwise for not finding the env variables
        from src.main.functions.order.create_order import calc_amount

        self.assertEqual(calc_amount(order_items), 0)


if __name__ == '__main__':
    main()

from unittest import TestCase, mock, main
import os


# Class for testing the calculated total amount of an order
# Mocking env variables bc it would otherwise throw an error for not finding them
@mock.patch.dict(os.environ, {'FRONTEND_ORIGIN': 'origin', 'REGION': 'region'})
class TestCalcAmount(TestCase):

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

        # Import is here bc it will throw an error otherwise for not finding the env variables
        from src.main.functions.order.payment import calc_amount

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
        from src.main.functions.order.payment import calc_amount

        self.assertEqual(calc_amount(order_items), 0)

    def test_calc_empty_order(self):
        order_items = []

        from src.main.functions.order.payment import calc_amount

        self.assertEqual(calc_amount(order_items), 0)


if __name__ == '__main__':
    main()

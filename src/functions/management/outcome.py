import logging
from src.functions.helper.Response import Response
from src.persistence import db_service


def outcome(event, context):
    table = db_service.get_orders_table()
    result = table.scan()

    if 'Items' in result:
        overall_revenue = 0
        sold_items = 0
        all_orders = result['Items']
        for order in all_orders:
            if order['status'] == 'accepted':
                logging.warning(order['amount'])
                overall_revenue += order['amount']

                for item in order['items']:
                    sold_items += item['quantity']

        response = Response(statusCode=200, body={'revenue': overall_revenue,
                                                  'sold_items': sold_items})

    else:
        response = Response(statusCode=404, body={'Message': 'Data not available.'})

    return response.to_json()

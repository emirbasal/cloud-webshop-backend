from src.main.helper.classes.response import Response
from src.main.helper.services import db_service
from src.main.helper.services.auth_service import is_authenticated


def outcome(event, context):
    if is_authenticated(event):
        table = db_service.get_orders_table()
        result = table.scan()

        if 'Items' in result:
            overall_revenue = 0
            sold_items = 0
            all_orders = result['Items']
            for order in all_orders:
                if order['status'] == 'accepted':
                    overall_revenue += order['amount']

                    for item in order['items']:
                        sold_items += item['quantity']

            response = Response(statusCode=200, body={'revenue': overall_revenue,
                                                      'sold_items': sold_items})

        else:
            response = Response(statusCode=404, body={'Message': 'Data not available'})
    else:
        response = Response(statusCode=403, body={'Message': 'Not authorized'})

    return response.to_json()

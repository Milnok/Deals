import csv, codecs

from django.core.exceptions import ValidationError

from .models import Deal, Customer, Gems


def save_file_to_bd(file):
    csvfile = csv.DictReader(codecs.iterdecode(file, 'utf-8'))

    field_names = ['customer', 'item', 'total', 'quantity', 'date']

    if not set(field_names) == set(csvfile.fieldnames):
        return {"Status": "Error",
                "Desc": "Invalid column names"}, 400

    deals_list = []
    customer_list = []
    for row in csvfile:
        row_customer = Customer.objects.get_or_create(username=row['customer'])
        row_deal = Deal(
            customer=row_customer[0],
            item=row['item'],
            total=row['total'],
            quantity=row['quantity'],
            date=row['date']
        )
        try:
            row_deal.clean_fields()
        except ValidationError:
            return {"Status": "Error",
                    "Desc": f"Error in row: {','.join(filter(None, [*row.values()]))}"}, 400
        row_customer[0].spent_money += int(row['total'])
        row_gem = Gems.objects.get_or_create(gem=row['item'])[0]
        row_gem.username.add(row_customer[0])

        customer_list.append(row_customer[0])
        deals_list.append(row_deal)
    Customer.objects.bulk_update(customer_list, fields=['spent_money'])
    Deal.objects.bulk_create(deals_list)

    return {'Status': 'OK'}, 200

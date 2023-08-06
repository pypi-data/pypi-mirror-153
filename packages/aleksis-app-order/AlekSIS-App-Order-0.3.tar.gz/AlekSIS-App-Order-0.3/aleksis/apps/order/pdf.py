import os

from blabel import LabelWriter

from .settings import BASE_DIR


def generate_order_labels(orders, temp_dir):
    records = []
    for order in orders:
        record = {
            "barcode": order.id,
            "full_name": order.full_name,
            "total": order.total,
            "items_count": order.items_count,
        }
        records.append(record)
    label_writer = LabelWriter(
        os.path.join(BASE_DIR, "order_label.html"),
        default_stylesheets=(os.path.join(BASE_DIR, "order_label_style.css"),),
    )
    label_writer.write_labels(records, target=os.path.join(temp_dir, "labels.pdf"))
    return os.path.join(temp_dir, "labels.pdf")


def generate_address_labels(orders, temp_dir):
    records = []
    for order in orders:
        record = {
            "sender": order.form.sender,
            "full_name": order.shipping_full_name,
            "second_address_row": order.second_address_row,
            "street": order.street,
            "housenumber": order.housenumber,
            "plz": order.plz,
            "place": order.place,
        }
        records.append(record)
    label_writer = LabelWriter(
        os.path.join(BASE_DIR, "address_label.html"),
        default_stylesheets=(os.path.join(BASE_DIR, "address_label_style.css"),),
    )
    label_writer.write_labels(records, target=os.path.join(temp_dir, "labels.pdf"))
    return os.path.join(temp_dir, "labels.pdf")

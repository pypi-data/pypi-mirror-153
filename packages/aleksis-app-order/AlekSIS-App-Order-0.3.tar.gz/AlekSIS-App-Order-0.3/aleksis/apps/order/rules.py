import rules

from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
)

from .models import OrderForm
from .util.predicates import has_order_perm

manage_orders_of_form_predicate = has_person & (
    has_global_perm("order.manage_orders") | has_object_perm("order.manage_orders_of_form")
)
rules.add_perm("order.manage_orders_of_form", manage_orders_of_form_predicate)

view_orders_predicate = has_person & (
    has_global_perm("order.manage.orders")
    | has_any_object("order.manage_orders_of_form", OrderForm)
)
rules.add_perm("order.view_orders", view_orders_predicate)

manage_order_predicate = has_person & (has_global_perm("order.manage_orders") | has_order_perm)
rules.add_perm("order.manage_order", manage_order_predicate)

show_menu_predicate = view_orders_predicate
rules.add_perm("order.show_menu", show_menu_predicate)

from django.contrib.auth.models import User

from rules import predicate

from aleksis.core.util.predicates import has_object_perm

from ..models import Order


@predicate
def has_order_perm(user: User, obj: Order) -> bool:
    return has_object_perm("order.manage_orders_of_form")(user, obj.form)

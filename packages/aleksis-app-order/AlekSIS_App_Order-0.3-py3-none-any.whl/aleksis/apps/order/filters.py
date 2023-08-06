from django.db.models.aggregates import Sum

import django_filters
from material import Layout, Row

from aleksis.apps.order.models import Order
from aleksis.core.util.core_helpers import queryset_rules_filter


class OrderFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr="icontains")
    items_count = django_filters.NumericRangeFilter(method="items_count_filter")

    def items_count_filter(self, queryset, name, value):
        return queryset.annotate(items_count_db=Sum("items__count")).filter(
            items_count_db__gte=value.start, items_count_db__lte=value.stop
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.layout = Layout(
            Row("form"),
            Row("full_name", "email"),
            Row("confirmed", "paid", "sent"),
            Row("processing_option", "items_count"),
        )

    @property
    def qs(self):
        parent = super().qs.order_by("full_name")
        user = getattr(self.request, "user", None)

        return queryset_rules_filter(user, parent, "order.manage_order")

    class Meta:
        model = Order
        fields = ["form", "full_name", "email", "confirmed", "paid", "sent", "processing_option"]

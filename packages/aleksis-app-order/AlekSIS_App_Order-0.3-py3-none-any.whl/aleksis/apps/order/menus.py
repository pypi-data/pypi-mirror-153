from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Orders"),
            "url": "#",
            "svg_icon": "mdi:cart-outline",
            "root": True,
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "order.show_menu",
                ),
            ],
            "submenu": [
                {
                    "name": _("List"),
                    "url": "list_orders",
                    "svg_icon": "mdi:receipt-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "order.view_orders",
                        ),
                    ],
                },
            ],
        }
    ]
}

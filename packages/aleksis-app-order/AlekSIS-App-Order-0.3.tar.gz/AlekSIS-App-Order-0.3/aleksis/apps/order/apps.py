from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.order"
    verbose_name = "AlekSIS — Order (Manage orders)"

    urls = {
        "Repository": "https://edugit.org/hansegucker/AlekSIS-App-Order",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2020, 2021], "Jonathan Weth", "dev@jonathanweth.de"),
        ([2021], "Hangzhi Yu", "yuha@katharineum.de"),
    )

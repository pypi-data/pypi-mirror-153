from django.contrib import admin

from guardian.admin import GuardedModelAdminMixin

from .models import Item, Order, OrderForm, OrderItem, ProcessingOption, ProcessingOptionPrice


class ItemInline(admin.TabularInline):
    model = Item


class ItemAdmin(admin.ModelAdmin):
    model = Item


admin.site.register(Item, ItemAdmin)


class OrderFormAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    model = OrderForm


admin.site.register(OrderForm, OrderFormAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["confirm_key", "form"]
    list_display = ["__str__", "submitted", "confirmed", "paid", "sent"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)


class ProcessingOptionPriceInline(admin.TabularInline):
    model = ProcessingOptionPrice


class ProcessingOptionAdmin(admin.ModelAdmin):
    model = ProcessingOption
    inlines = [ProcessingOptionPriceInline]


admin.site.register(ProcessingOption, ProcessingOptionAdmin)

from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel
from templated_email import send_templated_mail

from aleksis.core.mixins import ExtensibleModel


class Item(ExtensibleModel):
    short_name = models.CharField(max_length=255, verbose_name=_("Short name"), unique=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    notice = RichTextUploadingField(
        verbose_name=_("Notice"), help_text=_("Shown below the item"), blank=True
    )
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    max_count = models.IntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name=_("Maximum count of items")
    )

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class ProcessingOption(ExtensibleModel):
    short_name = models.CharField(max_length=255, verbose_name=_("Short name"), unique=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    notice = RichTextUploadingField(
        verbose_name=_("Notice"), help_text=_("Shown below the option"), blank=True
    )
    email_notice = RichTextUploadingField(
        verbose_name=_("Email notice"), help_text=_("Shown in the confirmation email"), blank=True
    )
    address_necessary = models.BooleanField(default=False, verbose_name=_("Adress necessary"))

    def get_price(self, count):
        for price in self.prices.order_by("price"):
            if price.min_count <= count <= price.max_count:
                return price.price
        return 0

    def __str__(self):
        return self.short_name


class ProcessingOptionPrice(ExtensibleModel):
    option = models.ForeignKey(
        ProcessingOption, models.CASCADE, related_name="prices", verbose_name=_("Processing option")
    )
    min_count = models.IntegerField(
        verbose_name=_("Min count of items"), validators=[MinValueValidator(0)]
    )
    max_count = models.IntegerField(
        verbose_name=_("Max count of items"), validators=[MinValueValidator(0)]
    )
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.option}: {self.min_count} <= x <= {self.max_count}"


class OrderForm(ExtensibleModel):
    title = models.CharField(max_length=255, verbose_name=_("Form title"))
    available_items = models.ManyToManyField(
        to=Item, related_name="forms", verbose_name=_("Available items")
    )
    available_processing_options = models.ManyToManyField(
        to=ProcessingOption, related_name="forms", verbose_name=_("Available processing options")
    )
    help_text = RichTextUploadingField(
        verbose_name=_("Help text"), help_text=_("Shown in the form's footer"), blank=True
    )
    from_email = models.EmailField(verbose_name=_("From email address"))
    from_name = models.CharField(verbose_name=_("From name"), max_length=255)
    access_code = models.CharField(max_length=2555, blank=True, verbose_name=_("Access code"))
    closed = models.BooleanField(default=False, verbose_name=_("Form closed for orders"))
    sender = models.TextField(blank=True, verbose_name=_("Sender"))

    def __str__(self):
        return self.title

    @property
    def email_sender(self):
        return f"{self.from_name} <{self.from_email}>"

    @property
    def total(self):
        return sum([order.total for order in self.orders.all()])

    @property
    def items_count(self):
        return sum([order.items_count for order in self.orders.all()])

    @property
    def confirmed_count(self):
        return sum([order.items_count for order in self.orders.all() if order.confirmed])

    @property
    def paid_count(self):
        return sum([order.items_count for order in self.orders.all() if order.paid])

    @property
    def sent_count(self):
        return sum([order.items_count for order in self.orders.all() if order.sent])

    @property
    def annotated_items(self):
        item_list = []
        for item in self.available_items.all():
            item.items_count = sum(
                [
                    order_item.count
                    for order_item in OrderItem.objects.filter(order__form=self, item=item)
                ]
            )
            item.confirmed_count = sum(
                [
                    order_item.count
                    for order_item in OrderItem.objects.filter(
                        order__form=self, item=item, order__confirmed=True
                    )
                ]
            )
            item.paid_count = sum(
                [
                    order_item.count
                    for order_item in OrderItem.objects.filter(
                        order__form=self, item=item, order__paid=True
                    )
                ]
            )
            item.sent_count = sum(
                [
                    order_item.count
                    for order_item in OrderItem.objects.filter(
                        order__form=self, item=item, order__sent=True
                    )
                ]
            )
            item.items_total = sum(
                [
                    order_item.total
                    for order_item in OrderItem.objects.filter(order__form=self, item=item)
                ]
            )
            item_list.append(item)
        return item_list

    class Meta:
        verbose_name = _("Order form")
        verbose_name_plural = _("Order forms")
        permissions = [("manage_orders_of_form", _("Can manage orders of form"))]


class Order(ExtensibleModel, TimeStampedModel):
    form = models.ForeignKey(
        to=OrderForm, on_delete=models.CASCADE, verbose_name=_("Order form"), related_name="orders"
    )
    full_name = models.CharField(max_length=255, verbose_name=_("First and last name"))
    email = models.EmailField(verbose_name=_("Email"))
    notes = models.TextField(verbose_name=_("Notes"), blank=True)

    submitted = models.BooleanField(default=False, verbose_name=_("Submitted"))
    confirmed = models.BooleanField(default=False, verbose_name=_("Confirmed"))
    confirm_key = models.TextField(verbose_name=_("Confirm key"), blank=True)
    paid = models.BooleanField(default=False, verbose_name=_("Paid"))
    sent = models.BooleanField(default=False, verbose_name=_("Sent"))

    processing_option = models.ForeignKey(
        ProcessingOption,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Selected processing option"),
    )
    shipping_full_name = models.CharField(
        verbose_name=_("First and last name"), max_length=255, blank=True
    )
    second_address_row = models.CharField(
        verbose_name=_("Second address row"), max_length=255, blank=True
    )
    street = models.CharField(verbose_name=_("Street"), max_length=255, blank=True)
    housenumber = models.CharField(verbose_name=_("Housenumber"), max_length=255, blank=True)
    plz = models.CharField(verbose_name=_("PLZ"), max_length=255, blank=True)
    place = models.CharField(verbose_name=_("Place"), max_length=255, blank=True)

    def get_confirm_url(self, request):
        return request.build_absolute_uri(reverse("confirm_order", args=[self.confirm_key]))

    @property
    def email_recipients(self):
        return [f"{self.full_name} <{self.email}>"]

    def send_overview(self, request):
        send_templated_mail(
            template_name="overview",
            from_email=self.form.email_sender,
            recipient_list=self.email_recipients,
            context={"order": self, "confirm_url": self.get_confirm_url(request)},
        )

    def confirm(self, request):
        self.confirmed = True
        self.save()
        send_templated_mail(
            template_name="confirmation",
            from_email=self.form.email_sender,
            recipient_list=self.email_recipients,
            context={"order": self, "confirm_url": self.get_confirm_url(request)},
        )

    def send_pay_confirmation(self):
        self.paid = True
        self.save()
        send_templated_mail(
            template_name="pay_confirmation",
            from_email=self.form.email_sender,
            recipient_list=self.email_recipients,
            context={"order": self},
        )

    def send_confirmation_reminder(self, request):
        send_templated_mail(
            template_name="confirmation_reminder",
            from_email=self.form.email_sender,
            recipient_list=self.email_recipients,
            context={"order": self, "confirm_url": self.get_confirm_url(request)},
        )

    def send_pay_reminder(self, request):
        send_templated_mail(
            template_name="pay_reminder",
            from_email=self.form.email_sender,
            recipient_list=self.email_recipients,
            context={"order": self},
        )

    def __str__(self):
        return f"{self.form}: {self.full_name} [{self.created}]"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.confirm_key:
            self.confirm_key = uuid4()

    @property
    def items_count(self):
        return self.items.aggregate(models.Sum("count")).get("count__sum")

    @property
    def processing_price(self):
        return self.processing_option.get_price(self.items_count) if self.processing_option else 0

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.total
        total += self.processing_price
        return total

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = [("manage_orders", _("Can manage orders"))]


class OrderItem(ExtensibleModel):
    count = models.IntegerField(verbose_name=_("Count"))
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, verbose_name=_("Item"))
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, verbose_name=_("Order"), related_name="items"
    )

    @property
    def total(self):
        return self.count * self.item.price

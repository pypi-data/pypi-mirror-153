from tempfile import TemporaryDirectory
from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.http.response import FileResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from rules.contrib.views import PermissionRequiredMixin

from aleksis.apps.order.filters import OrderFilter
from aleksis.apps.order.pdf import generate_address_labels, generate_order_labels
from aleksis.apps.order.tables import OrderTable
from aleksis.core.mixins import AdvancedDeleteView, AdvancedEditView
from aleksis.core.util.core_helpers import has_person, queryset_rules_filter
from aleksis.core.util.pdf import render_pdf

from .forms import (
    AccessForm,
    NotesForm,
    OrderActionForm,
    OrderFormForm,
    OrderItemFormSet,
    ProcessingOptionForm,
    ShippingAddressForm,
)
from .models import Order, OrderForm, OrderItem


class OrderFormView(DetailView):
    model = OrderForm
    template_name = "order/form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form_access_granted_key = f"order_access_{self.object.pk}"

        if self.object.closed:
            return redirect("index")

        access_granted = (
            has_person(self.request)
            or request.session.get("order")
            or request.session.get(form_access_granted_key)
            or not self.object.access_code.strip()
        )
        if access_granted:
            order = self.request.session.get("order")
            try:
                order = Order.objects.get(pk=order)
            except Order.DoesNotExist:
                order = None

            form = OrderFormForm(self.request.POST or None, instance=order)
            formset = OrderItemFormSet(
                self.request.POST or None,
                queryset=self.object.available_items.all(),
                prefix="order_item",
            )

            # Load order from session
            if order:
                counts_by_pk = {item.item.pk: item.count for item in order.items.all()}
                for item_form in formset:
                    item_form.fields["count"].initial = counts_by_pk.get(item_form.instance.pk, 0)

            context["form"] = form
            context["formset"] = formset

        if not access_granted:
            # Show access code form
            access_form = AccessForm(request.POST or None)
            context["access_form"] = access_form
            if request.method == "POST" and access_form.is_valid():
                if (
                    self.object.access_code.lower().strip()
                    == access_form.cleaned_data["access_code"]
                ):
                    request.session[form_access_granted_key] = True
                    return redirect("order_form", self.object.pk)
                else:
                    messages.error(request, _("Please enter the correct access code."))

            return render(request, "order/access.html", context)

        person = None
        if has_person(self.request):
            person = self.request.user.person
            form.fields["full_name"].disabled = True
            form.fields["full_name"].initial = person.addressing_name
            if person.email:
                form.fields["email"].disabled = True
                form.fields["email"].initial = person.email

        if self.request.method == "POST":
            items = []
            if form.is_valid():
                full_name = person.addressing_name if person else form.cleaned_data["full_name"]
                email = (
                    person.email if getattr(person, "email", None) else form.cleaned_data["email"]
                )

                # Get items
                if formset.is_valid():
                    total_count_of_items = 0
                    for item_form in formset:
                        # Calculate count
                        count = item_form.cleaned_data["count"]
                        total_count_of_items += count

                        if count > 0:
                            order_item = None

                            # Check for existing order item
                            if order:
                                try:
                                    order_item = OrderItem.objects.get(
                                        item=item_form.instance, order=order
                                    )
                                except OrderItem.DoesNotExist:
                                    pass

                            # New order item
                            if not order_item:
                                order_item = OrderItem(item=item_form.instance, count=count)

                            order_item.new_count = count
                            items.append(order_item)

                    # Check if there is at least one item
                    if total_count_of_items <= 0:
                        messages.error(self.request, _("You must order at least one item."))
                        return self.render_to_response(context)

                    # Get or create order
                    if not order:
                        order = Order.objects.create(
                            form=self.object, full_name=full_name, email=email
                        )
                    else:
                        order.full_name = full_name
                        order.email = email
                        order.save()

                    # Save order items
                    for item in items:
                        item.order = order
                        item.count = item.new_count
                        item.save()

                    # Set session and redirect
                    self.request.session["order"] = order.pk
                    return redirect("order_form_2", self.object.pk)
        # TODO DON'T GET FULL NAME AND EMAIL FROM FORM IF USER IS LOGGED IN

        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class OrderForm2View(DetailView):
    model = OrderForm
    template_name = "order/form2.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        order = self.request.session.get("order")
        try:
            self.order = Order.objects.get(pk=order)
        except Order.DoesNotExist:
            return redirect("order_form", self.object.pk)
        if self.order.form != self.get_object():
            return redirect("order_form_2", self.order.form.pk)

        if hasattr(self, "order"):
            context["order"] = self.order

            processing_form = ProcessingOptionForm(
                self.request.POST or None,
                initial={"processing_option": self.order.processing_option},
            )
            context["processing_form"] = processing_form

            processing_options = self.order.form.available_processing_options.all()
            for processing_option in processing_options:
                processing_option.price = processing_option.get_price(self.order.items_count)

            context["processing_options"] = processing_options

            shipping_address_form = ShippingAddressForm(
                self.request.POST or None,
                initial={
                    "full_name": self.order.shipping_full_name,
                    "second_address_row": self.order.second_address_row,
                    "street": self.order.street,
                    "housenumber": self.order.housenumber,
                    "plz": self.order.plz,
                    "place": self.order.place,
                },
            )
            context["shipping_address_form"] = shipping_address_form

            if self.request.method == "POST":
                if processing_form.is_valid():
                    processing_option = processing_form.cleaned_data["processing_option"]

                    if not processing_option.address_necessary or shipping_address_form.is_valid():
                        # WITH SHIPPING ADDRESS
                        self.order.processing_option = processing_option

                        if processing_option.address_necessary:
                            self.order.shipping_full_name = shipping_address_form.cleaned_data[
                                "full_name"
                            ]
                            self.order.second_address_row = shipping_address_form.cleaned_data[
                                "second_address_row"
                            ]
                            self.order.street = shipping_address_form.cleaned_data["street"]
                            self.order.housenumber = shipping_address_form.cleaned_data[
                                "housenumber"
                            ]
                            self.order.plz = shipping_address_form.cleaned_data["plz"]
                            self.order.place = shipping_address_form.cleaned_data["place"]

                        self.order.save()

                        return redirect("order_form_3", self.order.form.pk)
                else:
                    messages.error(request, _("Please select a processing option."))
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class OrderForm3View(DetailView):
    model = OrderForm
    template_name = "order/form3.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        order = self.request.session.get("order")
        try:
            self.order = Order.objects.get(pk=order)
        except Order.DoesNotExist:
            return redirect("order_form", self.object.pk)
        if self.order.form != self.get_object():
            return redirect("order_form_3", self.order.form.pk)

        context["order"] = self.order
        notes_form = NotesForm(request.POST or None, initial={"notes": self.order.notes})
        context["notes_form"] = notes_form
        if notes_form.is_valid():
            self.order.notes = notes_form.cleaned_data["notes"]
            self.order.save()
            return redirect("order_finished", self.order.form.pk)

        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class OrderFinishedView(DetailView):
    model = OrderForm
    template_name = "order/finished.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        order = self.request.session.get("order")
        try:
            self.order = Order.objects.get(pk=order)
        except Order.DoesNotExist:
            return redirect("order_form", self.get_object().pk)
        r = super().get(request, *args, **kwargs)
        if self.order.form != self.get_object():
            return redirect("order_finished", self.order.form.pk)
        return r

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if hasattr(self, "order"):
            context["order"] = self.order
            self.order.submitted = True
            self.order.save()
            self.order.send_overview(self.request)
            form_access_granted_key = f"order_access_{self.order.form.pk}"

            del self.request.session["order"]
            if form_access_granted_key in self.request.session:
                del self.request.session[form_access_granted_key]
        return context


class OrderConfirmView(View):
    def get(self, request: HttpRequest, key, **kwargs: Any) -> HttpResponse:
        try:
            self.order = Order.objects.get(confirm_key=key)
        except Order.DoesNotExist:
            return HttpResponseNotFound()
        if not self.order.confirmed:
            self.order.confirm(request)
        return render(request, "order/confirmed.html", context={"order": self.order})


class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    permission_required = "order.manage_order"
    template_name = "order/detail.html"


class OrderEditView(PermissionRequiredMixin, AdvancedEditView):
    model = Order
    fields = (
        "full_name",
        "email",
        "notes",
        "submitted",
        "confirmed",
        "paid",
        "sent",
        "processing_option",
        "shipping_full_name",
        "second_address_row",
        "street",
        "housenumber",
        "plz",
        "place",
    )
    permission_required = "order.manage_order"
    template_name = "order/edit.html"
    success_message = _("The order has been changed successfully.")
    success_url = reverse_lazy("list_orders")

    def post(self, request, *args, **kwargs):
        r = super().post(request, *args, **kwargs)

        order = self.get_object()

        if request.POST.get("mark-as-paid"):
            order.paid = True
            order.save()

        elif request.POST.get("mark-as-paid-email"):
            order.send_pay_confirmation()

        return r


class OrderDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    model = Order
    permission_required = "order.manage_order"
    template_name = "core/pages/delete.html"
    success_message = _("The order has been deleted successfully.")
    success_url = reverse_lazy("list_orders")


class OrderListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    table_class = OrderTable
    model = Order
    template_name = "order/list.html"
    permission_required = "order.view_orders"
    table_pagination = {"per_page": 50}

    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"].request = self.request
        context["forms"] = queryset_rules_filter(
            self.request.user, OrderForm.objects.all(), "order.manage_orders_of_form"
        )
        self.action_form = OrderActionForm(
            self.request, self.request.POST or None, queryset=self.get_queryset()
        )
        context["action_form"] = self.action_form
        return context

    def post(self, request, *args, **kwargs):
        r = self.get(request, *args, **kwargs)

        if "action" in self.request.POST and self.action_form.is_valid():
            self.action_form.execute()

        elif request.POST.get("all-action"):
            if request.POST.get("print"):
                return render_pdf(request, "order/list_print.html", self.get_context_data())
            elif request.POST.get("packing-lists"):
                return render_pdf(request, "order/packing_lists.html", self.get_context_data())

        # Action for a single object
        elif request.POST.get("single-action-pk"):
            order = get_object_or_404(Order, pk=request.POST.get("single-action-pk"))

            if request.POST.get("mark-as-paid"):
                order.paid = True
                order.save()

            elif request.POST.get("mark-as-paid-email"):
                order.send_pay_confirmation()

            elif request.POST.get("mark-as-sent"):
                order.sent = True
                order.save()

        # Actions for all objects
        elif request.POST.get("all-action"):
            if request.POST.get("mark-as-paid"):
                self.object_list.update(paid=True)

            elif request.POST.get("mark-as-paid-email"):
                self.object_list.update(paid=True)
                for order in self.object_list:
                    order.send_pay_confirmation()
            elif request.POST.get("mark-as-sent"):
                self.object_list.update(sent=True)

            elif request.POST.get("labels"):
                with TemporaryDirectory() as temp_dir:
                    filename = generate_order_labels(self.object_list, temp_dir)
                    f = open(filename, "rb")
                    return FileResponse(f, filename="labels.pdf")
            elif request.POST.get("address-labels"):
                with TemporaryDirectory() as temp_dir:
                    filename = generate_address_labels(self.object_list, temp_dir)
                    f = open(filename, "rb")
                    return FileResponse(f, filename="labels.pdf")
        return r

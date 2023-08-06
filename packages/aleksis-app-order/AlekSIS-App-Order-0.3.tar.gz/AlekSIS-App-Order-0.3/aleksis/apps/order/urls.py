from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.OrderListView.as_view(), name="list_orders"),
    path("list/<int:pk>/", views.OrderDetailView.as_view(), name="show_order"),
    path("list/<int:pk>/edit/", views.OrderEditView.as_view(), name="edit_order"),
    path("list/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="delete_order"),
    path("<int:pk>/", views.OrderFormView.as_view(), name="order_form"),
    path("<int:pk>/2/", views.OrderForm2View.as_view(), name="order_form_2"),
    path("<int:pk>/3/", views.OrderForm3View.as_view(), name="order_form_3"),
    path("<int:pk>/finished/", views.OrderFinishedView.as_view(), name="order_finished"),
    path("confirm/<str:key>/", views.OrderConfirmView.as_view(), name="confirm_order"),
]

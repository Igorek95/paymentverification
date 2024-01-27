from django.urls import path

from .apps import PaymentConfig
from .swagger import schema_view
from .views import (
    PaymentRequisiteListView, PaymentRequisiteDetailView,
    PaymentRequisiteCreateView, PaymentRequisiteUpdateView, PaymentRequisiteDeleteView,
    PaymentRequestListView, PaymentRequestDetailView,
    PaymentRequestCreateView, PaymentRequestUpdateView, PaymentRequestDeleteView,
    home, about, contacts, CreateInvoice, GetInvoiceStatus
)

app_name = PaymentConfig.name

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),

    path('create_invoice/', CreateInvoice.as_view(), name='create-invoice'),
    path('get_invoice_status/<int:invoice_id>/', GetInvoiceStatus.as_view(), name='get-invoice-status'),


    path('payment-requisites/', PaymentRequisiteListView.as_view(), name='payment_requisite_list'),
    path('payment-requisite/<int:pk>/', PaymentRequisiteDetailView.as_view(), name='payment_requisite_detail'),
    path('payment-requisite/new/', PaymentRequisiteCreateView.as_view(), name='payment_requisite_create'),
    path('payment-requisite/<int:pk>/edit/', PaymentRequisiteUpdateView.as_view(), name='payment_requisite_update'),
    path('payment-requisite/<int:pk>/delete/', PaymentRequisiteDeleteView.as_view(), name='payment_requisite_delete'),

    path('payment-requests/', PaymentRequestListView.as_view(), name='payment_request_list'),
    path('payment-request/<int:pk>/', PaymentRequestDetailView.as_view(), name='payment_request_detail'),
    path('payment-request/new/', PaymentRequestCreateView.as_view(), name='payment_request_create'),
    path('payment-request/<int:pk>/edit/', PaymentRequestUpdateView.as_view(), name='payment_request_update'),
    path('payment-request/<int:pk>/delete/', PaymentRequestDeleteView.as_view(), name='payment_request_delete'),
]

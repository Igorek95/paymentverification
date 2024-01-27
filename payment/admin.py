from django.contrib import admin

from payment.models import PaymentRequisite, PaymentRequest


@admin.register(PaymentRequisite)
class PaymentRequisiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_type', 'account_type', 'owner_name', 'phone_number', 'limit')
    search_fields = ('owner_name', 'phone_number')


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'requisites')
    list_filter = ('status',)
    search_fields = ('requisites__owner_name',)

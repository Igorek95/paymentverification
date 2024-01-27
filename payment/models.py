from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class PaymentRequisite(models.Model):
    """
    Модель реквизитов для оплаты.
    """

    PAYMENT_CHOICES = [
        ('Card', 'Карта'),
        ('BankAccount', 'Платежный счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(_("Тип платежа"), max_length=50, choices=PAYMENT_CHOICES)
    account_type = models.CharField(_("Тип карты/счета"), max_length=50)
    owner_name = models.CharField(_("ФИО владельца"), max_length=100)
    phone_number = models.CharField(_("Номер телефона"), max_length=15)
    limit = models.DecimalField(_("Лимит"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.owner_name} - {self.payment_type}"

    class Meta:
        verbose_name = _("Реквизит для оплаты")
        verbose_name_plural = _("Реквизиты для оплаты")


class PaymentRequest(models.Model):
    """
    Модель заявки на оплату.
    """

    STATUS_CHOICES = [
        ('Pending', 'Ожидает оплаты'),
        ('Paid', 'Оплачена'),
        ('Cancelled', 'Отменена'),
    ]

    amount = models.DecimalField(_("Сумма"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default='Pending')
    requisites = models.ForeignKey('payment.PaymentRequisite', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Заявка на оплату #{self.id} - {self.status}"

    class Meta:
        verbose_name = _("Заявка на оплату")
        verbose_name_plural = _("Заявки на оплату")

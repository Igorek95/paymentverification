# Generated by Django 4.2.9 on 2024-01-26 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('Card', 'Карта'), ('BankAccount', 'Платежный счет')], max_length=50, verbose_name='Тип платежа')),
                ('account_type', models.CharField(max_length=50, verbose_name='Тип карты/счета')),
                ('owner_name', models.CharField(max_length=100, verbose_name='ФИО владельца')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Лимит')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Реквизит для оплаты',
                'verbose_name_plural': 'Реквизиты для оплаты',
            },
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('Pending', 'Ожидает оплаты'), ('Paid', 'Оплачена'), ('Cancelled', 'Отменена')], default='Pending', max_length=20, verbose_name='Статус')),
                ('requisites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.paymentrequisite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка на оплату',
                'verbose_name_plural': 'Заявки на оплату',
            },
        ),
    ]

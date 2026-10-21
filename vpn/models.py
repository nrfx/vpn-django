from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tariff(models.Model):
    name = models.CharField('Название', max_length=100)
    duration_days = models.PositiveIntegerField('Срок действия (дни)')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    device_limit = models.PositiveSmallIntegerField('Лимит устройств', default=1)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    started_at = models.DateTimeField('Начало', auto_now_add=True)
    expires_at = models.DateTimeField('Истекает')
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} — {self.tariff.name}'

class Device(models.Model):
    class DeviceType(models.TextChoices):
        MOBILE = 'mobile', 'Телефон'
        DESKTOP = 'desktop', 'Компьютер'
        ROUTER = 'router', 'Роутер'
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='devices', verbose_name='Подписка')
    name = models.CharField('Название устройства', max_length=100)
    device_type = models.CharField(
        'Тип',
        max_length=50,
        choices=DeviceType.choices,
        default=DeviceType.MOBILE
    )
    connected_at = models.DateTimeField('Дата подключения', auto_now_add=True)
    last_active = models.DateTimeField('Последняя активность', null=True, blank=True)

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return f'{self.name} ({self.subscription.user.username})'

class Profile(models.Model):
    class Role(models.IntegerChoices):
        USER = 0, 'Пользователь'
        ADMIN = 1, 'Администратор'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField('Баланс', max_digits=8, decimal_places=2, default=0)
    role = models.IntegerField('Роль', choices=Role.choices, default=Role.USER)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'В обработке'
        SUCCESS = 'success', 'Успешно'
        FAILED = 'failed', 'Ошибка'
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подписка')
    amount = models.DecimalField('Сумма', max_digits=8, decimal_places=2)
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user.username} — {self.amount}'

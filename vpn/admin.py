from django.contrib import admin

from vpn.models import Tariff, Subscription, Device, Profile, Payment


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'price', 'device_limit')
    list_filter = ('duration_days',)
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tariff', 'started_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'tariff')
    search_fields = ('user__username',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'subscription', 'connected_at', 'last_active')
    list_filter = ('device_type',)
    search_fields = ('name', 'subscription__user__username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'subscription', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

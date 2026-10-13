from rest_framework import serializers

from vpn.models import Tariff, Subscription, Device, Profile, Payment


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'name', 'duration_days', 'price', 'device_limit']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'tariff', 'started_at', 'expires_at', 'is_active']
        read_only_fields = ['started_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'subscription', 'name', 'device_type', 'connected_at', 'last_active']
        read_only_fields = ['connected_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'balance']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'subscription', 'amount', 'status', 'created_at']
        read_only_fields = ['created_at']

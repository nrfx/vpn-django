from django.contrib.auth.models import User
from rest_framework import serializers

from vpn.models import Tariff, Subscription, Device, Profile, Payment


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'name', 'duration_days', 'price', 'device_limit']


class SubscriptionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    tariff_name = serializers.CharField(source='tariff.name', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_name', 'tariff', 'tariff_name',
                  'started_at', 'expires_at', 'is_active']
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


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    active_subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'password',
                  'balance', 'role', 'active_subscriptions']
        read_only_fields = ['user']

    def get_active_subscriptions(self, obj):
        return obj.user.subscription_set.filter(is_active=True).count()

    def validate_username(self, value):
        users = User.objects.filter(username=value)
        if self.instance:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise serializers.ValidationError('Пользователь с таким логином уже существует')
        return value

    def validate(self, attrs):
        # пароль обязателен только при создании
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Укажите пароль'})
        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data.get('email', ''),
            password=password,
        )
        # профиль уже создал сигнал post_save, просто заполняем его
        profile = user.profile
        for field, value in validated_data.items():
            setattr(profile, field, value)
        profile.save()
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        if password:
            user.set_password(password)
        user.save()
        return super().update(instance, validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'subscription', 'amount', 'status', 'created_at']
        read_only_fields = ['created_at']

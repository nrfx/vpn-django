from rest_framework.viewsets import ModelViewSet

from vpn.models import Tariff, Subscription, Device, Profile, Payment
from vpn.serializers import (
    TariffSerializer,
    SubscriptionSerializer,
    DeviceSerializer,
    ProfileSerializer,
    ClientSerializer,
    PaymentSerializer,
)


class TariffViewSet(ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ClientViewSet(ModelViewSet):
    queryset = Profile.objects.select_related('user').order_by('id')
    serializer_class = ClientSerializer

    def perform_destroy(self, instance):
        # каскадное удаление 
        instance.user.delete()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

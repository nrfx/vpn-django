from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from vpn.models import Tariff, Subscription, Device, Profile, Payment
EXPIRES = "2030-01-01T00:00:00Z"

class TariffViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        tariff = baker.make("vpn.Tariff")
        r = self.client.get('/api/tariffs/')
        data = r.json()
        assert len(data) == 1
        assert data[0]['id'] == tariff.id
        assert data[0]['name'] == tariff.name

    def test_create_tariff(self):
        r = self.client.post('/api/tariffs/', {
            "name": "Базовый", "duration_days": 30,
            "price": "199.00", "device_limit": 3,
        })
        assert r.status_code == 201
        new = Tariff.objects.get(id=r.json()['id'])
        assert new.name == "Базовый"
        assert Tariff.objects.count() == 1

    def test_delete_tariff(self):
        tariffs = baker.make("vpn.Tariff", 10)
        self.client.delete(f'/api/tariffs/{tariffs[3].id}/')
        data = self.client.get('/api/tariffs/').json()
        assert len(data) == 9
        assert tariffs[3].id not in [i['id'] for i in data]

    def test_update_tariff(self):
        tariff = baker.make("vpn.Tariff")
        r = self.client.patch(f'/api/tariffs/{tariff.id}/', {"name": "Новое имя"})
        assert r.status_code == 200
        tariff.refresh_from_db()
        assert tariff.name == "Новое имя"

    def test_retrieve(self):
        tariff = baker.make("vpn.Tariff")
        r = self.client.get(f'/api/tariffs/{tariff.id}/')
        assert r.status_code == 200
        assert r.json()['name'] == tariff.name

class SubscriptionViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = 'json'

    def test_list(self):
        sub = baker.make("vpn.Subscription")
        data = self.client.get('/api/subscriptions/').json()
        assert len(data) == 1
        assert data[0]['id'] == sub.id
        assert data[0]['user'] == sub.user.id
        assert data[0]['tariff'] == sub.tariff.id
        assert data[0]['is_active'] == sub.is_active

    def test_retrieve(self):
        sub = baker.make("vpn.Subscription")
        r = self.client.get(f'/api/subscriptions/{sub.id}/')
        assert r.status_code == 200
        assert r.json()['id'] == sub.id
        assert r.json()['tariff'] == sub.tariff.id

    def test_create(self):
        user = baker.make("auth.User")
        tariff = baker.make("vpn.Tariff")
        r = self.client.post('/api/subscriptions/', {
            "user": user.id, "tariff": tariff.id, "expires_at": EXPIRES,
        })
        assert r.status_code == 201
        assert Subscription.objects.count() == 1
        new = Subscription.objects.get(id=r.json()['id'])
        assert new.user == user
        assert new.tariff == tariff
        assert new.is_active is True

    def test_update(self):
        sub = baker.make("vpn.Subscription", is_active=True)
        r = self.client.patch(f'/api/subscriptions/{sub.id}/', {"is_active": False})
        assert r.status_code == 200
        sub.refresh_from_db()
        assert sub.is_active is False

    def test_delete(self):
        subs = baker.make("vpn.Subscription", _quantity=10)
        r = self.client.delete(f'/api/subscriptions/{subs[3].id}/')
        assert r.status_code == 204
        data = self.client.get('/api/subscriptions/').json()
        assert len(data) == 9
        assert subs[3].id not in [i['id'] for i in data]


class DeviceViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        sub = baker.make("vpn.Subscription")
        device = baker.make("vpn.Device", subscription=sub)
        data = self.client.get('/api/devices/').json()
        assert len(data) == 1
        assert data[0]['id'] == device.id
        assert data[0]['name'] == device.name
        assert data[0]['subscription'] == sub.id

    def test_retrieve(self):
        device = baker.make("vpn.Device")
        r = self.client.get(f'/api/devices/{device.id}/')
        assert r.status_code == 200
        assert r.json()['name'] == device.name
        assert r.json()['device_type'] == device.device_type

    def test_create(self):
        sub = baker.make("vpn.Subscription")
        r = self.client.post('/api/devices/', {
            "subscription": sub.id, "name": "Мой телефон", "device_type": "mobile",
        })
        assert r.status_code == 201
        assert Device.objects.count() == 1
        new = Device.objects.get(id=r.json()['id'])
        assert new.name == "Мой телефон"
        assert new.device_type == "mobile"
        assert new.subscription == sub

    def test_update(self):
        device = baker.make("vpn.Device", device_type="mobile")
        r = self.client.patch(f'/api/devices/{device.id}/', {"device_type": "router"})
        assert r.status_code == 200
        device.refresh_from_db()
        assert device.device_type == "router"

    def test_delete(self):
        devices = baker.make("vpn.Device", _quantity=10)
        r = self.client.delete(f'/api/devices/{devices[3].id}/')
        assert r.status_code == 204
        data = self.client.get('/api/devices/').json()
        assert len(data) == 9
        assert devices[3].id not in [i['id'] for i in data]


class ProfileViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        profile = baker.make("vpn.Profile")
        profile.refresh_from_db()
        data = self.client.get('/api/profiles/').json()
        assert len(data) == 1
        assert data[0]['id'] == profile.id
        assert data[0]['user'] == profile.user.id
        assert data[0]['balance'] == str(profile.balance)

    def test_retrieve(self):
        profile = baker.make("vpn.Profile")
        r = self.client.get(f'/api/profiles/{profile.id}/')
        assert r.status_code == 200
        assert r.json()['user'] == profile.user.id

    def test_create(self):
        user = baker.make("auth.User")
        r = self.client.post('/api/profiles/', {"user": user.id, "balance": "150.50"})
        assert r.status_code == 201
        assert Profile.objects.count() == 1
        new = Profile.objects.get(id=r.json()['id'])
        assert new.user == user
        assert str(new.balance) == "150.50"

    def test_update(self):
        profile = baker.make("vpn.Profile", balance=0)
        r = self.client.patch(f'/api/profiles/{profile.id}/', {"balance": "300.00"})
        assert r.status_code == 200
        profile.refresh_from_db()
        assert str(profile.balance) == "300.00"

    def test_delete(self):
        profiles = baker.make("vpn.Profile", _quantity=10)
        r = self.client.delete(f'/api/profiles/{profiles[3].id}/')
        assert r.status_code == 204
        data = self.client.get('/api/profiles/').json()
        assert len(data) == 9
        assert profiles[3].id not in [i['id'] for i in data]


class PaymentViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        payment = baker.make("vpn.Payment")
        data = self.client.get('/api/payments/').json()
        assert len(data) == 1
        assert data[0]['id'] == payment.id
        assert data[0]['user'] == payment.user.id
        assert data[0]['amount'] == str(payment.amount)
        assert data[0]['status'] == payment.status

    def test_retrieve(self):
        payment = baker.make("vpn.Payment")
        r = self.client.get(f'/api/payments/{payment.id}/')
        assert r.status_code == 200
        assert r.json()['id'] == payment.id

    def test_create(self):
        user = baker.make("auth.User")
        r = self.client.post('/api/payments/', {
            "user": user.id, "amount": "199.00", "status": "success",
        })
        assert r.status_code == 201
        assert Payment.objects.count() == 1
        new = Payment.objects.get(id=r.json()['id'])
        assert new.user == user
        assert str(new.amount) == "199.00"
        assert new.status == "success"
        assert new.subscription is None

    def test_update(self):
        payment = baker.make("vpn.Payment", status="pending")
        r = self.client.patch(f'/api/payments/{payment.id}/', {"status": "failed"})
        assert r.status_code == 200
        payment.refresh_from_db()
        assert payment.status == "failed"

    def test_delete(self):
        payments = baker.make("vpn.Payment", _quantity=10)
        r = self.client.delete(f'/api/payments/{payments[3].id}/')
        assert r.status_code == 204
        data = self.client.get('/api/payments/').json()
        assert len(data) == 9
        assert payments[3].id not in [i['id'] for i in data]
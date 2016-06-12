from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .models import Driver, Ride, DayStatement, WeekStatement, MonthStatement

class DriverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )

    def test_get_driver_name(self):
        winona = Driver.objects.get(email='wr@g.com')
        self.assertEqual(winona.get_name(), 'Winona Ryder')

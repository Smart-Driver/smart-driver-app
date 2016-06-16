import json
import datetime
import requests
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, Client, RequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from .models import Driver, Ride, DayStatement, WeekStatement, MonthStatement
from .views import DriverViewSet, RideViewSet, DayStatementViewSet
from .views import WeekStatementViewSet, MonthStatementViewSet


class DriverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.session = requests.Session()
        Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )

        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/login_response.txt',
                'r'
                ) as f:
            self.login_response_text = f.read()

        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/54d1a166-8755-f64f-3e37-a3f4b53a08f4.json',
                'r'
                ) as f:
            self.data = json.loads(f.read())

    def test_get_driver_name(self):
        winona = Driver.objects.get(email='wr@g.com')
        self.assertEqual(winona.get_name(), 'Winona Ryder')

    def test_get_csrf_token(self):
        token = Driver.get_csrf_token(self.session)
        self.assertIs(type(token), str)

    def test_get_u_user_id(self):
        sample_response = self.client.get('/')
        sample_response.text = self.login_response_text
        winona = Driver.objects.get(email='wr@g.com')
        winona.get_u_user_id(sample_response)
        self.assertEqual(winona.u_user_id, 'x1x2x3x4x5')

    def test_get_statement_ids(self):
        sample_response = self.client.get('/')
        sample_response.text = self.login_response_text
        ids = Driver.get_statement_ids(sample_response)
        self.assertIs(len(ids), 41)

    ''' the grab_data() function calls 8 other functions in all classes to save
    related objects from one json into to the relational database. It is
    tested further in other test classes '''
    def test_grab_data(self):
        winona = Driver.objects.get(email='wr@g.com')
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        self.assertTrue(winona.ride_set.count() > 0)

    def test_get_new_statements(self):
        ids = ['54d1a166-8755-f64f-3e37-a3f4b53a08f4', 'new_id']
        winona = Driver.objects.get(email='wr@g.com')
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        new_statement_id = winona.get_new_statement_ids(ids)
        self.assertEqual(new_statement_id, ['new_id'])


class RideTestCase(TestCase):
    def setUp(self):
        winona = Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )
        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/54d1a166-8755-f64f-3e37-a3f4b53a08f4.json',
                'r'
                ) as f:
            self.data = json.loads(f.read())
        self.session = requests.Session()
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        self.ride = winona.ride_set.get(
            trip_id='33d66c37-2b7b-4fc5-8622-4944f3068125')

    def test_get_stats_in_grab_data(self):
        self.assertEqual(self.ride.date, datetime.date(2015, 11, 16))
        self.assertEqual(self.ride.status, 'completed')
        self.assertEqual(self.ride.begintrip_at, datetime.datetime(
                2015, 11, 16, 19, 50, 22, tzinfo=datetime.timezone.utc))
        self.assertEqual(self.ride.dropoff_at, datetime.datetime(
                2015, 11, 16, 20, 11, 57, tzinfo=datetime.timezone.utc))
        self.assertEqual(self.ride.total_earned, Decimal('26.40'))
        self.assertEqual(self.ride.distance, Decimal('14.86'))
        self.assertEqual(self.ride.request_at, datetime.datetime(
                2015, 11, 16, 19, 43, 46, tzinfo=datetime.timezone.utc))
        self.assertEqual(self.ride.duration, datetime.timedelta(0, 1294))

    def test_assign_month_in_grab_data(self):
        self.assertEqual(self.ride.month_statement,
                         MonthStatement.objects.get(month_name="November '15"))

    def test_assign_week_in_grab_data(self):
        self.assertEqual(self.ride.week_statement, WeekStatement.objects.get(
            starting_at=datetime.date(2015, 11, 16)))

    def test_assign_day_in_grab_data(self):
        self.assertEqual(self.ride.day_statement, DayStatement.objects.get(
            date=datetime.date(2015, 11, 16)))


class DayStatementTestCase(TestCase):
    def setUp(self):
        winona = Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )
        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/54d1a166-8755-f64f-3e37-a3f4b53a08f4.json',
                'r'
                ) as f:
            self.data = json.loads(f.read())
        self.session = requests.Session()
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        self.day_statement = winona.daystatement_set.get(
            date=datetime.date(2015, 11, 16))

    def test_calculate_day_stats(self):
        self.assertEqual(self.day_statement.total_rides, 10)
        self.assertEqual(self.day_statement.total_earned, Decimal('181.93'))
        self.assertEqual(self.day_statement.rate_per_ride, Decimal('18.19'))
        self.assertEqual(self.day_statement.time_worked,
                         datetime.timedelta(0, 31398))
        self.assertEqual(self.day_statement.rate_per_hour, Decimal('20.86'))


class WeekStatementTestCase(TestCase):
    def setUp(self):
        winona = Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )
        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/54d1a166-8755-f64f-3e37-a3f4b53a08f4.json',
                'r'
                ) as f:
            self.data = json.loads(f.read())
        self.session = requests.Session()
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        self.week_statement = winona.weekstatement_set.get(
            starting_at=datetime.date(2015, 11, 16))

    def test_calculate_week_stats(self):
        self.assertEqual(self.week_statement.total_earned, Decimal('455.10'))
        self.assertEqual(self.week_statement.total_rides, 37)
        self.assertEqual(self.week_statement.rate_per_ride, Decimal('12.30'))
        self.assertEqual(self.week_statement.rate_per_hour, Decimal('13.54'))
        self.assertEqual(self.week_statement.rate_per_day, Decimal('113.78'))

    def test_associate_months(self):
        self.assertEqual(
            self.week_statement.month_statement.first().month_name,
            "November '15")


class MonthStatementTestCase(TestCase):
    def setUp(self):
        winona = Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
            )
        with open(
            '/Users/kathrynjackson/Code/smart_driver_notes/54d1a166-8755-f64f-3e37-a3f4b53a08f4.json',
                'r'
                ) as f:
            self.data = json.loads(f.read())
        self.session = requests.Session()
        with patch(
                'driver_app.models.Driver.get_statement',
                return_value=self.data):
            winona.grab_data(self.session,
                             ['54d1a166-8755-f64f-3e37-a3f4b53a08f4'])
        self.month_statement = winona.monthstatement_set.get(
            starting_at=datetime.date(2015, 11, 1))

    def test_calculate_month_stats_total_earned(self):
        self.assertEqual(self.month_statement.total_earned, Decimal('455.10'))
        self.assertEqual(self.month_statement.total_rides, 37)
        self.assertEqual(self.month_statement.rate_per_ride, Decimal('12.30'))
        self.assertEqual(self.month_statement.rate_per_hour, Decimal('13.54'))
        self.assertEqual(self.month_statement.rate_per_day, Decimal('113.78'))


class APITestCase(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            u_user_id='123abc',
            user=User.objects.create(username='wr@g.com'),
            email='wr@g.com',
            first_name='WINONA',
            last_name='RYDER'
        )
        self.ride = Ride.objects.create(
            driver=self.driver,
            trip_id='abc123',
            status='completed',
            total_earned=6.50,
            distance=2.3,
            date=datetime.date(2015, 8, 1),
            request_at=datetime.datetime(2015, 8, 1, 15, 50, 1, 39252),
            begintrip_at=datetime.datetime(2015, 8, 1, 15, 51, 1, 39252),
            dropoff_at=datetime.datetime(2015, 8, 1, 15, 52, 1, 39252),
            duration=datetime.timedelta(0, 500)
        )
        self.day = DayStatement.objects.create(
            driver=self.driver,
            total_rides=10,
            total_earned=32.50,
            date=datetime.date(2015, 8, 1),
            weekday=datetime.date(2015, 8, 1).weekday(),
            time_worked=datetime.timedelta(0, 14400),
            rate_per_ride=3.25,
            rate_per_hour=8.13,
        )
        self.week = WeekStatement.objects.create(
            driver=self.driver,
            starting_at=datetime.date(2015, 7, 27),
            ending_at=datetime.date(2015, 7, 27) + datetime.timedelta(days=6),
            total_earned=500.00,
            rate_per_ride=10.00,
            rate_per_hour=20.00,
            rate_per_day=50.00,
            total_rides=50,
            statement_id='1a2b3c'
        )
        self.month = MonthStatement.objects.create(
            driver=self.driver,
            starting_at=datetime.date(2015, 8, 1),
            ending_at=datetime.date(2015, 8, 31),
            month_name=datetime.date(2015, 8, 1).strftime('%B \'%y'),
            total_earned=2000.00,
            rate_per_day=50.00,
            rate_per_ride=10.00,
            rate_per_hour=15.00,
            total_rides=200
        )
        self.ride.day_statement = self.day
        self.ride.week_statement = self.week
        self.ride.month_statement = self.month
        self.ride.save()
        self.day.week_statement = self.week
        self.day.month_statement = self.month
        self.day.save()
        self.week.month_statement = [self.month]
        self.week.save()

        self.user = User.objects.get(username='wr@g.com')
        self.factory = RequestFactory()
        self.driver_endpoint = DriverViewSet.as_view({'get': 'retrieve'})
        self.ride_endpoint = RideViewSet.as_view({'get': 'retrieve'})
        self.day_statement_endpoint = DayStatementViewSet.as_view(
            {'get': 'retrieve'})
        self.week_statement_endpoint = WeekStatementViewSet.as_view(
            {'get': 'retrieve'})
        self.month_statement_endpoint = MonthStatementViewSet.as_view(
            {'get': 'retrieve'})

    def test_driver_endpoint_status_ok(self):
        request = self.factory.get('/api/drivers/')
        force_authenticate(request, self.user)
        response = self.driver_endpoint(request, pk=self.driver.pk)
        self.assertEqual(response.status_code, 200)

    def test_driver_endpoint_response_data(self):
        request = self.factory.get('/api/drivers/')
        force_authenticate(request, user=self.user)
        response = self.driver_endpoint(request, pk=self.driver.pk)
        self.assertEqual(response.data, {
            "url": "http://testserver/api/drivers/" + str(self.driver.pk) + "/",
            "first_name": "WINONA",
            "last_name": "RYDER"
            })

    def test_ride_endpoint_status_ok(self):
        request = self.factory.get('/api/rides/')
        force_authenticate(request, user=self.user)
        response = self.ride_endpoint(request, pk=self.ride.trip_id)
        self.assertEqual(response.status_code, 200)

    def test_ride_endpoint_response_data(self):
        request = self.factory.get('/api/rides/')
        force_authenticate(request, user=self.user)
        response = self.ride_endpoint(request, pk=self.ride.trip_id)
        self.assertEqual(response.data, {
            "date": "2015-08-01",
            "status": "completed",
            "total_earned": "6.50",
            "request_at": "2015-08-01T15:50:01.039252Z"
            })

    def test_day_statement_endpoint_status_ok(self):
        request = self.factory.get('/api/day_statements/')
        force_authenticate(request, user=self.user)
        response = self.day_statement_endpoint(request, pk=self.day.pk)
        self.assertEqual(response.status_code, 200)

    def test_day_statement_endpoint_response_data(self):
        request = self.factory.get('/api/day_statements/')
        force_authenticate(request, user=self.user)
        response = self.day_statement_endpoint(request, pk=self.day.pk)
        self.assertEqual(response.data, {
            "date": "Aug 01, 2015",
            "weekday": "Saturday",
            "total_earned": "$32.50",
            "time_worked": "04:00:00",
            "rate_per_hour": "$8.13",
            "total_rides": 10,
            "rate_per_ride": "$3.25"
            })

    def test_week_statement_endpoint_status_ok(self):
        request = self.factory.get('/api/week_statements/')
        force_authenticate(request, user=self.user)
        response = self.week_statement_endpoint(request, pk=self.week.pk)
        self.assertEqual(response.status_code, 200)

    def test_week_statement_endpoint_response_data(self):
        request = self.factory.get('/api/week_statements/')
        force_authenticate(request, user=self.user)
        response = self.week_statement_endpoint(request, pk=self.week.pk)
        self.assertEqual(response.data, {
            "starting_at": "07-27-15",
            "ending_at": "08-02-15",
            "total_earned": "$500.00",
            "rate_per_day": "$50.00",
            "rate_per_hour": "$20.00",
            "total_rides": 50,
            "rate_per_ride": "$10.00"
            })

    def test_month_statement_endpoint_status_ok(self):
        request = self.factory.get('/api/month_statements/')
        force_authenticate(request, user=self.user)
        response = self.month_statement_endpoint(request, pk=self.month.pk)
        self.assertEqual(response.status_code, 200)

    def test_month_statement_endpoint_response_data(self):
        request = self.factory.get('/api/month_statements/')
        force_authenticate(request, user=self.user)
        response = self.month_statement_endpoint(request, pk=self.month.pk)
        self.assertEqual(response.data, {
            "month_name": "August '15",
            "total_earned": "2000.00",
            "rate_per_day": "50.00",
            "rate_per_hour": "15.00",
            "total_rides": 200,
            "rate_per_ride": "10.00"
            })

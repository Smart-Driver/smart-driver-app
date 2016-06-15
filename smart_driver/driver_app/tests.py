import datetime
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

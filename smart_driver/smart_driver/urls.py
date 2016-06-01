from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from driver_app import views


router = routers.DefaultRouter()
router.register(r'rides', views.RideViewSet)
router.register(r'week_statements', views.WeekStatementViewSet)
router.register(r'day_statements', views.DayStatementViewSet)
router.register(r'drivers', views.DriverViewSet)

app_name = 'driver_app'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

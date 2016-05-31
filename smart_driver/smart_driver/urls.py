from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from driver_app import views


router = routers.DefaultRouter()
router.register(r'rides', views.RideViewSet)
router.register(r'statements', views.StatementViewSet)
router.register(r'drivers', views.DriverViewSet)


urlpatterns = [
    #url(r'^$', 'smart_driver.views.home', name='home'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

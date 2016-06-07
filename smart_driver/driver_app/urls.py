from django.conf.urls import url
from . import views

app_name = 'driver_app'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^logout/$', views.logout_view, name='logout'),
]

# (r'^profile/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'})

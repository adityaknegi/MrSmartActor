from django.conf.urls import url
from smartassistant import views

urlpatterns = [
    url(r'^api/smartassistant/get_one_movies_list', views.get_one_movies_list),
    url(r'^api/smartassistant/get_movies_set', views.get_movies_set)
]
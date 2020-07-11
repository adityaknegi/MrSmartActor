from django.conf.urls import url
from smartassistant import views

urlpatterns = [
    url(r'^api/smartassistant/get_movie_list$', views.get_movie_list)
]
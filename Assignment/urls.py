from django.conf.urls import url
from . import views



urlpatterns = [

    url(r'^register/$', views.UserRegister.as_view()),
    url(r'^login/$', views.UserLogin.as_view()),
    url(r'^content-post/$', views.ContentPost.as_view()),
    url(r'^content-get/$', views.ContentGet.as_view()),
    url(r'^activate/$', views.UserActivate.as_view()),



    ]

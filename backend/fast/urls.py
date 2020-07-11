from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'fast'


router = routers.DefaultRouter()
router.register('post', views.CreateListPost, basename='post')


urlpatterns = [

    path("login/", views.LoginAPIView.as_view(), name='login'),
    path("list/post/", views.ListPostGAPIView.as_view(), name='list-post'),
    path("email/<str:to>/<str:by>", views.send_email, name='email'),

]
urlpatterns += router.urls

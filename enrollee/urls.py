from django.urls import path, include

from . import views

app_name = 'enrollee'


urlpatterns = [
    path('register', views.CreateUserView.as_view(), name="create"),
    path('login/', views.CreateTokenView.as_view(), name="token"),
    path('documents/', views.CreateUpdateEnrollment.as_view(), name="enrollment"),
    path('user/', views.UserDataView.as_view(), name="user"),
]
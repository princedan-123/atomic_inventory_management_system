from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserCrud)

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('', include(router.urls))
]
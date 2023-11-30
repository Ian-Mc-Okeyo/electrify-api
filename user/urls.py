from django.urls import path
from .views import *

urlpatterns = [
    path("register", RegisterView.as_view(), name='register'),
    path("login", LoginView.as_view(), name='login'),
    path("day-data", DataToday.as_view(), name='daily-data'),
    path("test", Test.as_view(), name='test'),
    path("weeks-data", WeeksData.as_view(), name='weeks-data'),
    path("receive-data", ReceiveData.as_view(), name='receive-data')
]
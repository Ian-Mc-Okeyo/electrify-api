from django.urls import path
from .views import *

urlpatterns = [
    path("register", RegisterView.as_view(), name='register'),
    path("login", LoginView.as_view(), name='login'),
    path("day-data/<str:userEmail>/<str:meterNumber>", DataToday.as_view(), name='daily-data'),
    path("test", Test.as_view(), name='test'),
    path("weeks-data/<str:userEmail>/<str:meterNumber>", WeeksData.as_view(), name='weeks-data'),
    path("month-data/<str:userEmail>/<str:meterNumber>", MonthlyData.as_view(), name='month-data'),
    path("receive-data", ReceiveData.as_view(), name='receive-data'),
    path("dashboard-data/<str:userEmail>/<str:meterNumber>", DashboardView.as_view(), name='dashboard-data')
]
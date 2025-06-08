from django.urls import path
from .views import TruckUnloadView

urlpatterns = [
    path('', TruckUnloadView.as_view(), name='index'),
]

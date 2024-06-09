from django.urls import path
from trackpi.views import FedexTrackingView


urlpatterns=[
    path('track/',FedexTrackingView.as_view()),
  
]
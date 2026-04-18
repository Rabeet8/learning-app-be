from django.urls import path
from .views import evaluate_speech

urlpatterns = [
    path('evaluate/', evaluate_speech),
]
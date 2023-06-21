from django.urls import path, include
from .views import Index, store

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
]

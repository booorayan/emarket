from django.urls import path, include
from .views import Index, Login, logout, store

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
]

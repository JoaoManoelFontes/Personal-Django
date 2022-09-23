from unicodedata import name
from django.urls import path
from .views import create_room, update_room, rooms, room, login

urlpatterns = [
    path('', rooms, name="home"),
    path('room/<int:roomId>', room, name="room"),
    path('create', create_room, name="create"),
    path('update/<int:roomId>', update_room, name="update"),
    path('login', login, name='login')

]
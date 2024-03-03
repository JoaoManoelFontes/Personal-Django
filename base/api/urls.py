from django.urls import path
from .views import views

urlpatterns = [
    path("", views.getRooms),
    path("room/<str:roomId>/", views.getRoom),
    path("topics/<str:topicId>/", views.getRoomsForTopic),
]

from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Room, Message, Topic
from .form import RoomForm

# Create your views here.


def rooms(request):
    if request.method == "POST":
        room = Room.objects.get(pk=request.POST["delete"])
        room.delete()

    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    # buscar_dados()
    return render(
        request,
        "home.html",
        {"rooms": rooms, "topics": topics, "room_count": room_count},
    )


def room(request, roomId):
    room = Room.objects.get(pk=roomId)
    if request.method == "POST":
        Message.objects.create(
            room=room, user=request.user, body=request.POST.get("message")
        )
        return redirect("room", roomId=roomId)

    messages = Message.objects.filter(room=room)
    return render(request, "room.html", {"room": room, "messages": messages})


def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("/")
    return render(request, "room_form.html", {"form": RoomForm()})


def update_room(request, roomId):
    room = Room.objects.get(pk=roomId)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("/admin")

    return render(request, "room_form.html", {"form": RoomForm(instance=room)})


def delete(request):
    room = Room.objects.get(pk=1)
    if request.method == "POST":
        room.delete()


def login(request):
    return JsonResponse("Login", safe=False)

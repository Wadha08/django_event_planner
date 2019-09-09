from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import UserSignup, UserLogin, EventForm ,BookingForm
from datetime import datetime
from .models import Event, Booking
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")

class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")



def create_event(request):
    if request.user.is_anonymous:
        messages.warning(request, "You have to log in first!")
        return redirect("home")
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES or None)
        if form.is_valid():
            event=form.save(commit=False)
            event.owner = request.user
            event.save()
            messages.success(request, "Successfully Created!")
            return redirect('list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create.html', context)


def event_list(request):
    if request.user.is_anonymous:
        messages.warning(request, "You have to log in first!")
        return redirect("home")
    events = Event.objects.filter(date__gte=datetime.today())
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(title__icontains = query)|
            Q(owner__username__icontains = query)|
            Q(description__icontains =query)).distinct()
    context = {
        "events": events,
    }
    return render(request, 'list.html', context)


def event_detail(request,event_id):
    if request.user.is_anonymous:
        messages.warning(request, "You have to log in first!")
        return redirect("home")
    event = Event.objects.get(id=event_id)
    users = Booking.objects.filter(event__id = event_id)
    context = {
        "event": event,
        "users": users,
    }
    return render(request, 'detail.html', context)


def event_edit(request,event_id):
    event=Event.objects.get(id=event_id)
    owner = event.owner
    if owner != request.user:
         messages.warning(request, "You are not authorized to edit this event!")
         return redirect("list")
    form = EventForm(instance = event)
    if request.method == "POST":
        form = EventForm(request.POST , instance=event)
        if form.is_valid():
            form.save()
            return redirect('list')
    context = {
        "event": event,
        "form": form,
    }
    return render(request, 'edit.html', context)


def dashboard(request):
    if request.user.is_anonymous:
        messages.warning(request, "You have to log in first!")
        return redirect("home")
    my_events = Event.objects.filter(owner = request.user)
    past_events = Booking.objects.filter(user = request.user, event__date__lt=datetime.today())
    context = {
        "my_events" : my_events,
        "past_events": past_events,
    }
    return render (request, "dashboard.html", context)


def booking(request, event_id):
    if request.user.is_anonymous:
        messages.warning(request, "You have to log in first!")
        return redirect("home")
    form = BookingForm()
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        form = BookingForm(request.POST, request.FILES or None)
        if form.is_valid():
            book=form.save(commit=False)
            book.user = request.user
            book.event = event
            seats = int(book.num_seats)
            if seats > event.get_seats_left():
                messages.warning(request, "You are exceeding the seats limit!")
                return redirect('list')
            book.save()
            messages.success(request, "Successfully booked!")
            return redirect('list')
        print (form.errors)
    context = {
    "form": form,
    "event": event,
    }
    return render(request, 'booking.html', context)









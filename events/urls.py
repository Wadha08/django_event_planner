from django.urls import path
from events import views

urlpatterns = [
	path('home/', views.home, name='home'),

	path('events/create/', views.create_event, name = 'create'),
	path('events/list/', views.event_list, name = 'list'),
	path('events/detail/<int:event_id>/', views.event_detail, name = 'detail'),
	path('events/edit/<int:event_id>/', views.event_edit, name = 'edit'),
	path('events/booking/<int:event_id>/', views.booking, name = 'booking'),


	path('dashboard/', views.dashboard, name = 'dashboard'),

    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),


]
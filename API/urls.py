
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from API import views 

app_name='API'

urlpatterns = [
 
    path('API/list/', views.EventList.as_view(), name = 'API_list'), 
    path('API/org/list/<int:owner_id>/', views.OrgList.as_view(), name = 'API_org_list'),
    path('API/booking/list/', views.BookingList.as_view(), name = 'API_booking_list'),
    path('API/create/', views.CreateEvent.as_view(), name = 'API_create'),
    path('API/update/<int:event_id>/', views.UpdateEvent.as_view(), name = 'API_update'),
    path('API/detail/<int:event_id>/', views.EventDetails.as_view(), name = 'API_detail'),

    path('API/register/', views.Register.as_view(), name="register"),
    path('API/login/', TokenObtainPairView.as_view(), name='login'),

]
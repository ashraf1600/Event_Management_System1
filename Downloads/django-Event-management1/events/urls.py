from django.urls import path
from . import views

urlpatterns = [
    # Dashboard er jonno URL
    path('', views.dashboard, name='dashboard'),
    
    # Event er jonno URL
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/update/', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    
    # Participant er jonno URL
    path('participants/', views.participant_list, name='participant_list'),
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    
    # Category  er jonno URL
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]


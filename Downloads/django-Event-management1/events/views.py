from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from django.db.models import Prefetch

from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm, EventSearchForm

def dashboard(request):
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).count()
    past_events = Event.objects.filter(date__lt=timezone.now().date()).count()
    todays_events = Event.objects.filter(date=timezone.now().date()).select_related('category')
    filter_type = request.GET.get('filter', 'today')
    
    if filter_type == 'all':
        filtered_events = Event.objects.all().select_related('category')
        filter_title = "All Events"
    elif filter_type == 'upcoming': 
        filtered_events = Event.objects.filter(date__gte=timezone.now().date()).select_related('category')
        filter_title = "Upcoming Events"
    elif filter_type == 'past':
        filtered_events = Event.objects.filter(date__lt=timezone.now().date()).select_related('category')
        filter_title = "Past Events"
    else:
        filtered_events = todays_events
        filter_title = "Today's Events"
    filtered_events = filtered_events.annotate(participant_count=Count('participants'))
    
    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
        'filtered_events': filtered_events,
        'filter_title': filter_title,
        'filter_type': filter_type,
    }
    
    return render(request, 'dashboard.html', context)
def event_list(request):
    form = EventSearchForm(request.GET)
    events = Event.objects.all().select_related('category').annotate(participant_count=Count('participants'))
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) | 
                Q(location__icontains=search_query)
            )
        
        if category:
            events = events.filter(category=category)
            
        if start_date:
            events = events.filter(date__gte=start_date)
            
        if end_date:
            events = events.filter(date__lte=end_date)
    
    context = {
        'events': events,
        'form': form,
    }
    
    return render(request, 'event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    
    context = {
        'event': event,
    }
    
    return render(request, 'event_detail.html', context)

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'event_form.html', {'form': form, 'title': 'Create Event'})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'event_form.html', {'form': form, 'title': 'Update Event'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'event_confirm_delete.html', {'event': event})
def participant_list(request):
    participants = Participant.objects.all().prefetch_related('events')
    
    context = {
        'participants': participants,
    }
    
    return render(request, 'participant_list.html', context)

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant created successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    
    return render(request, 'participant_form.html', {'form': form, 'title': 'Create Participant'})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant updated successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    
    return render(request, 'participant_form.html', {'form': form, 'title': 'Update Participant'})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant deleted successfully!')
        return redirect('participant_list')
    
    return render(request, 'participant_confirm_delete.html', {'participant': participant})
def category_list(request):
    categories = Category.objects.all().annotate(event_count=Count('events'))
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'category_list.html', context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form, 'title': 'Create Category'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'category_form.html', {'form': form, 'title': 'Update Category'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'category_confirm_delete.html', {'category': category})


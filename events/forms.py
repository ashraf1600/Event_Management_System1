from django import forms
from django.utils import timezone
from .models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date') 
        
        if date and date < timezone.now().date():
            if date < timezone.now().date():
                raise forms.ValidationError("Event date cannot be in the past.")
        
        return cleaned_data

class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Participant.objects.filter(email=email).exists() and not self.instance.pk:
            raise forms.ValidationError("A participant with this email already exists.")
        return email

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exists() and not self.instance.pk:
            raise forms.ValidationError("A category with this name already exists.")
        return name

class EventSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search events')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Filter by category'
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Start date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='End date' 
    )


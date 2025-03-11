from django.contrib import admin
from .models import Event, Participant, Category

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location', 'category')
    list_filter = ('date', 'category')
    search_fields = ('name', 'location')
    date_hierarchy = 'date'

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    filter_horizontal = ('events',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Category, CategoryAdmin)


from django.contrib import admin
#from django.db import models
# Register your models here.
from .models import Suggestion 

class SuggestionAdmin(admin.ModelAdmin):
   list_display = ['content_object','user','value']
   search_fields = ['user__username']
   raw_id_fields = ['user']
   readonly_fields = ['content_object']


admin.site.register(Suggestion, SuggestionAdmin)

# Register your models here.

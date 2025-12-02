from django.shortcuts import render

from suggestions.models import Suggestion
# Create your views here.

#def home_view(request):
 #   context = {}
 #   user = request.user
 #   if not user.is_authenticated:
 #       return render(request, 'home.html' , context )
 #   context['endless_path'] = '/'
 #   qs = Suggestion.objects.filter(user=user,
 #           did_rate = False)
 #   context['object'] = qs.order_by('?').first()['content_object']
 #   if request.htmx:
 #       return render(request, "movies/snippet/infinite.html" , context)
 #   return render(request, "dashboard/main.html", context)
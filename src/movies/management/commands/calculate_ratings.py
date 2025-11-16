from django.core.management.base  import BaseCommand
from django.contrib.auth import get_user_model


#from cfehome import utils as cfehome_utils
#from movies.models import Movie

#from ratings.models import Rating
#from movies.tasks import task_calculate_movie_ratings
from ratings.tasks import task_update_movie_ratings
User = get_user_model() # Get the user model

class Command(BaseCommand):
     
      
      def handle(self, *args, **options):
           task_update_movie_ratings()
           #all = options.get('all')
           #count = options.get('count')
           #task_calculate_movie_ratings(all=all, count=count)

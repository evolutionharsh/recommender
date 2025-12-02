from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from movies.models import Movie
from profiles import utils as profile_utils
from . import utils as ml_utils

@shared_task
def train_surprise_model_task():
     ml_utils.train_surprise_model()

@shared_task
def batch_users_prediction_task(user_ids=None, start_page=0 , offset=50 ,
          max_pages=100):
    model = ml_utils.load_model()
    Suggestion = apps.get_model('suggestions','Suggestion')
    ctype = ContentType.objects.get(app_label = 'movies' , model = 'movie')
    end_page = start_page + offset
    #recent_user_ids = profile_utils.get_recent_users()
    if user_ids is None:
       user_ids = profile_utils.get_recent_users()
    movie_ids = Movie.objects.all().popular().values_list('id',
                                                flat=True)[start_page:
                                                           end_page]
    recently_suggested = Suggestion.objects.get_recently_suggested(movie_ids, user_ids)
    new_suggestion = []
    for movie_id in movie_ids:
        users_done = recently_suggested.get(f"{movie_id}") or []
        for u in user_ids:
            if u in user_ids:
                print(movie_id, 'is done for', u , 'user')
                continue
            pred = model.predict(uid=u, iid=movie_id).est
            #print(u, movie_id, pred)
            data = {
                'user_id' : u,
                'object_id' : movie_id,
                'value' : pred ,
                'content_type' : ctype
            }
            new_suggestion.append(
                Suggestion(**data)
            )
    Suggestion.objects.bulk_create(new_suggestion, ignore_conflicts=True)
    if end_page < max_pages:
        return batch_users_prediction_task(start_page = end_page - 1)


#@shared_task
#def batch_single_user_predictions_task(user_id =1 ,start_page=0 , offset=250 ,
         # max_pages=1):
    #model = ml_utils.load_model()
    #end_page = start_page + offset
    #recent_user_ids = profile_utils.get_recent_users()
   # recent_user_ids = [user_id]
   # movie_ids = Movie.objects.all().popular().values_list('id',
                                                #flat=True)[start_page:
                                                          # end_page]
   # for movie_id in movie_ids:
    #    for u in recent_user_ids:
    #        pred = model.predict(uid=u, iid=movie_id).est
    #        print(u, movie_id, pred)
    #if end_page < max_pages:
   #return batch_users_prediction_task(user_ids=[user_id],start_page=start_page , offset=offset ,
    #      max_pages=max_pages)
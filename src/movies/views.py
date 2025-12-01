from django.views import generic

# Create your views here.

from .models import Movie

SORTING_CHOICES = {
    "popular": "popular" ,
    "unpopular": "unpopular" ,
    "top rated": "-rating_avg" ,
    "low rated": "rating_avg" ,
    "recent": "-release_date" ,
    "old": "release_date"
}

class MovieListView(generic.ListView):
    #template_name = 'movies/list.html'
    paginate_by = 100
    
    def get_queryset(self):
        request = self.request
        sort = request.session.get('movie_sort_order') or request.session.get
        ('movie_sort_order') or 'popular'
        queryset = Movie.objects.all() #.order_by(default_sort)
        
        #sort = request.GET.get('sort')
        if sort is not None:
           request.session['movie_sort_order'] = sort
           if sort == 'popular':
               return queryset.popular()
           elif sort == 'unpopular':
               return queryset.popular(reverse=True) 
           queryset = queryset.order_by(sort) 
        return queryset

    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/list.html']
        return ['movies/list.html']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
       # print(context['object_list'])
        request = self.request
        user = request.user
        context['sorting_choices'] = SORTING_CHOICES
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            #qs = user.rating_set.filter(active = True, object_id__in=object_ids)
            context['my_ratings'] = user.rating_set.movies().as_object_dict(object_ids=object_ids)
        #context['my_ratings']
        return context
   
movie_list_view = MovieListView.as_view()


class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'

    #context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
       # print(context['object_list'])
        request = self.request
        user = request.user
        if user.is_authenticated:
            object = context['object']
            object_ids = [object.id]
            #qs = user.rating_set.filter(active = True, object_id__in=object_ids)
            context['my_ratings'] = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            #context['my_ratings']
        return context


movie_detail_view = MovieDetailView.as_view()


class MovieInfiniteRatingView(MovieDetailView):
    def get_object(self):
        user = self.request.user
        #exclude_ids=[]
        #if user.is_authenticated:
        #    exclude_ids=[x.object_id for x in user.rating_set.filter(active=True)]
        return Movie.objects.all().order_by("?").first()
    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/infinite.html']
        return ['movies/infinite-view.html']
    

movie_infinite_rating_view = MovieInfiniteRatingView.as_view()

class MoviePopularView(MovieDetailView):
    def get_object(self):
        user = self.request.user
        exclude_ids=[]
        if user.is_authenticated:
            exclude_ids=[x.object_id for x in user.rating_set.filter(active=True)]
        movie_id_options = Movie.objects.all().popular().exclude(id__in=exclude_ids).values_list('id',flat = True)[:250]
        return Movie.objects.filter(id__in=movie_id_options).order_by("?").first()
    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/infinite.html']
        return ['movies/infinite-view.html']
    

movie_popular_view = MoviePopularView.as_view()



from rest_framework.viewsets import ModelViewSet#The actions provided by the ModelViewSet class are
# .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().


from .models import Actor, Movie, Comment
from .serializers import ActorSerializer, MovieSerializer, CommentSerializer, RegisterSerializer
from rest_framework.decorators import action#action - the name of the current action (e.g., list, create)
from rest_framework.response import Response# allows you to return content that can be rendered into multiple content types, depending on the client request.
from rest_framework.authentication import TokenAuthentication#To use the TokenAuthentication scheme you'll need to configure the authentication classes to include
# TokenAuthentication, and additionally include rest_framework.authtoken in your INSTALLED_APPS setting:
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters, mixins, viewsets#The mixin classes provide the actions that are used to provide the basic view behavior.
# Note that the mixin classes provide action methods rather than defining the handler methods,
from rest_framework.pagination import LimitOffsetPagination


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['imdb']
    search_fields = ['name', 'genre']
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['POST'] , url_path='add-actor')#if detail is True it is about object, if it is false it is about quesryset
    def add_actor(self, request, pk,  *args, **kwargs):
        movie = self.get_object()#it gets the object from Movie Model according to its id
        actor_id = request.data['actor_id']#request.data is equal to request.POST, we will give property to 'actor_id'
        actor = Actor.objects.get(pk=actor_id)
        movie.actor.add(actor)
        movie.save()
        return Response({'status':'success'})

    @action(detail=True, methods=['POST'], url_path='remove-actor')
    def remove_actor(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data['actor_id']#we will give id number to 'actor_id' in insomnia like: 'actor_id': 2,it means we can write anything instead of 'actor_id'. maybe 'actors_id' or anything
        actor = Actor.objects.get(pk=actor_id)
        movie.actor.remove(actor)
        movie.save()
        return Response({'status': 'success'})


    @action(detail=True, methods=['GET'])
    def actors(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = ActorSerializer(movie.actor.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def watched(self, request, *args, **kwargs):
        movie = self.get_object()#it retrieves the movie object from the queryset according to it's id number
        #with transaction.atomic():#it is used when two users open the movie in similar time.
        movie.watched += 1
        movie.save()
        return Response({'status':'success'})

    @action(detail=False, methods=['GET'])
    def top(self,request, *args, **kwargs):
        movies = self.get_queryset()
        movies = movies.order_by('-watched')[:10]
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class  = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self,serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()






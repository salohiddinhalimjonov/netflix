from django.test import TestCase, Client
from app.models import Actor, Movie
class TestMovieViewSet(TestCase):
    def setUp(self) -> None:

        self.actor = Actor.objects.create(name='Jackie Chan', birth_date='1954-4-7')
        self.movie = Movie.objects.create(name='Oltin To\'qmoq', year='2008-01-01')
        self.movie.actor.add(self.actor)
        self.client = Client()

    def test_get_all_movies(self):

        response = self.client.get('/movies/')
        data = response.data
        self.assertEquals(len(data), 1)
        self.assertIsNotNone(data[0]['id'])
        self.assertEquals(data[0]['name'], 'Oltin To\'qmoq')
        self.assertEquals(response.status_code, 200)

    def test_search_movie(self):
        response = self.client.get('/movies/?search=Oltin To\'qmoq')
        data = response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['name'], 'Oltin To\'qmoq' )

    def test_order_movie(self):
        response = self.client.get('/movies/?ordering=imdb')
        data = response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data[0]['name'], 'Oltin To\'qmoq')
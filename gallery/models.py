from django.db import models
from .gauth import Role, User, UserManager


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ADMIN)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ADMIN, password, **extra_fields)


class Admin(User):
    objects = AdminManager()
    class Meta(User.Meta):
        proxy = True


class ArtistManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ARTIST)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ARTIST, password, **extra_fields)


class Artist(User):
    objects = ArtistManager()
    class Meta(User.Meta):
        proxy = True


class OrganizerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ORGANIZER)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ORGANIZER, password, **extra_fields)


class Organizer(User):
    objects = OrganizerManager()
    class Meta(User.Meta):
        proxy = True

class Genre(models.Model):
    name = models.CharField(max_length=32)


class Drawing(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/')
    name = models.CharField(max_length=32)
    description = models.TextField()
    artist = models.ForeignKey(Artist, related_name='drawings', related_query_name='drawing')
    genres = models.ManyToManyField(Genre, related_name='drawings', related_query_name='drawing')
    hidden = models.BooleanField('спрятано', default=False)


class Exhibition(models.Model):
    images = models.ManyToManyField(
        Drawing,
        related_name='exhibitions',
        related_query_name='exhibition',
    )
    organizer = models.ForeignKey(Organizer, related_name='exhibitions', related_query_name='exhibition')
    name = models.CharField(max_length=32)
    publish_date = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, related_name='exhibitions', related_query_name='exhibition')

from django.core.urlresolvers import reverse
from django.db import models
from .gauth import Role, User, UserManager
from django.utils.translation import ugettext_lazy as _


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

    def get_absolute_url(self):
        return reverse('artist-detail',args=[self.pk])


class OrganizerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ORGANIZER)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ORGANIZER, password, **extra_fields)


class Organizer(User):
    objects = OrganizerManager()
    class Meta(User.Meta):
        proxy = True
        verbose_name = _('organizer')
        verbose_name_plural = _('organizers')

class Genre(models.Model):
    name = models.CharField(max_length=32)
    __str__ = lambda self: self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Drawing(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/')
    name = models.CharField(max_length=32)
    description = models.TextField()
    artist = models.ForeignKey(Artist, related_name='drawings', related_query_name='drawing')
    genres = models.ManyToManyField(Genre, related_name='drawings', related_query_name='drawing')
    hidden = models.BooleanField('спрятано', default=False)
    date_uploaded = models.DateTimeField('загружено', auto_now=True)
    __str__ = lambda self: self.name

    def get_absolute_url(self):
        return reverse('drawing-view',args=[self.pk])

    class Meta:
        verbose_name = _('drawing')
        verbose_name_plural = _('drawings')



class Exhibition(models.Model):
    drawings = models.ManyToManyField(
        Drawing,
        related_name='exhibitions',
        related_query_name='exhibition',
    )
    organizer = models.ForeignKey(Organizer, related_name='exhibitions', related_query_name='exhibition')
    name = models.CharField(max_length=32)
    publish_date = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    genres = models.ManyToManyField(
        Genre,
        through='ExhibitionGenre',
        through_fields=('exhibition', 'genre'),
        related_name='exhibitions2',
        related_query_name='exhibition2'
    )
    description = models.TextField('описание выставки')

    def get_absolute_url(self):
        return reverse('exhibition-view',args=[self.pk])

    class Meta:
        verbose_name = _('exhibition')
        verbose_name_plural = _('exhibitions')


class ExhibitionGenre(models.Model):
    exhibition = models.ForeignKey(Exhibition)
    genre = models.ForeignKey(Genre)
    priority = models.PositiveIntegerField()

    class Meta:
        unique_together = ('exhibition', 'genre')
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
import re
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
        verbose_name = 'администратор'
        verbose_name_plural = 'администраторы'

    def get_absolute_url(self):
        return reverse('admin:index')


class ArtistManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ARTIST)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ARTIST, password, **extra_fields)


class Artist(User):
    objects = ArtistManager()
    class Meta(User.Meta):
        proxy = True
        verbose_name = 'художник'
        verbose_name_plural = 'художники'

    def get_absolute_url(self):
        return reverse('artist-detail',args=[self.pk])

    def owns_drawing(self, drawing):
        if not isinstance(drawing, Drawing):
            return Drawing.objects.filter(pk=drawing, artist=self.id).exists()
        else :
            return drawing.artist_id == self.id


class OrganizerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ORGANIZER)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ORGANIZER, password, **extra_fields)


class Organizer(User):
    objects = OrganizerManager()
    class Meta(User.Meta):
        proxy = True
        verbose_name = 'организатор выставок'
        verbose_name_plural = 'организаторы выставок'

    def get_absolute_url(self):
        return reverse('organizer-detail', args=[self.pk])

    def owns_exhibition(self, exhibition):
        if not isinstance(exhibition, Exhibition):
            return Exhibition.objects.filter(pk=exhibition, organizer=self.id).exists()
        else:
            return exhibition.organizer_id == self.id


class Genre(models.Model):
    name = models.CharField('название', max_length=32)
    __str__ = lambda self: self.name

    def get_related_exhibitions_page_url(self):
        return '%s?genre=%d' % (reverse('exhibitions-index'), self.pk)

    def get_related_drawings_page_url(self):
        return '%s?genre=%d' % (reverse('drawings-index'), self.pk)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class DrawingWithCountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(Count('exhibition'))


name_regex = re.compile(r'^[А-Яа-яA-Za-z\w\s\.\,]+$')


class Drawing(models.Model):
    image = models.ImageField('изображение', upload_to='images/%Y/%m/')
    name = models.CharField('название', max_length=32,
        validators=[
            validators.RegexValidator(name_regex,
                                      _('Название должно содержать '
                                        'только буквы латинского или '
                                        'кириллического алфавита.'),
                                      'invalid'),
        ],
    )
    description = models.TextField('детальное описание')
    artist = models.ForeignKey(Artist,
                               verbose_name='художник',
                               related_name='drawings',
                               related_query_name='drawing')
    genres = models.ManyToManyField(
        Genre,
        through='DrawingGenre',
        through_fields=('drawing', 'genre'),
        related_name='drawings',
        related_query_name='drawing',
        verbose_name='жанры'
    )
    hidden = models.BooleanField('картина спрятана', default=False)
    date_uploaded = models.DateTimeField('загружено', auto_now=True)
    __str__ = lambda self: self.name

    objects = DrawingWithCountManager()

    def get_absolute_url(self):
        return reverse('drawing-detail',args=[self.pk])

    def get_related_exhibitions_page_url(self):
        return '%s?drawing=%d' % (reverse('exhibitions-index'), self.pk)

    class Meta:
        verbose_name = 'картина'
        verbose_name_plural = 'картины'


class Exhibition(models.Model):
    drawings = models.ManyToManyField(
        Drawing,
        related_name='exhibitions',
        related_query_name='exhibition',
    )
    organizer = models.ForeignKey(Organizer,
                                  verbose_name='организатор',
                                  related_name='exhibitions',
                                  related_query_name='exhibition')
    name = models.CharField('название', max_length=32,
        validators=[
            validators.RegexValidator(name_regex,
                                      _('Название должно содержать '
                                        'только буквы латинского или '
                                        'кириллического алфавита.'),
                                      'invalid'),
        ],
    )
    description = models.TextField('детальное описание')
    publish_date = models.DateField('дата публикации', auto_now=True)
    approved = models.BooleanField('выставка проверена', default=False)
    genres = models.ManyToManyField(
        Genre,
        verbose_name='жанры',
        through='ExhibitionGenre',
        through_fields=('exhibition', 'genre'),
        related_name='exhibitions',
        related_query_name='exhibition'
    )

    def get_absolute_url(self):
        return reverse('exhibition-detail',args=[self.pk])

    def __str__(self):
        return '%d %s' % (self.pk, self.name)

    class Meta:
        verbose_name = 'выставка'
        verbose_name_plural = 'выставки'
        ordering = ('id',)


class DrawingGenre(models.Model):
    drawing = models.ForeignKey(Drawing)
    genre = models.ForeignKey(Genre, verbose_name='жанр')
    priority = models.PositiveIntegerField('приоритет')

    def __str__(self):
        return "%d: drawing:%d, num:%d, genre:%d" %\
               (self.pk, self.drawing_id, self.priority, self.genre_id)

    class Meta:
        unique_together = ('drawing', 'genre')
        ordering = ('drawing_id', 'priority')



class ExhibitionGenre(models.Model):
    exhibition = models.ForeignKey(Exhibition)
    genre = models.ForeignKey(Genre, verbose_name='жанр')
    priority = models.PositiveIntegerField('приоритет')

    def __str__(self):
        return "%d: xzibit:%d, num:%d, genre:%d" %\
               (self.pk, self.exhibition_id, self.priority, self.genre_id)

    class Meta:
        unique_together = ('exhibition', 'genre')
        ordering = ('exhibition_id', 'priority')

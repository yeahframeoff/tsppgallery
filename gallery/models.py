import datetime
from django import forms
from django.core import validators
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count, QuerySet
import re
from .gauth import Role, User, UserManager
from django.utils.translation import ugettext_lazy as _


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ADMIN)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ADMIN,
                                   password, **extra_fields)


class Admin(User):
    objects = AdminManager()
    class Meta(User.Meta):
        proxy = True
        verbose_name = 'администратор'
        verbose_name_plural = 'администраторы'

    def get_absolute_url(self):
        return reverse('admin:index')

    def add_genre(self, genre):
        if isinstance(genre, str):
            genre = Genre(name=genre)
        elif not isinstance(genre, Genre):
            raise ValueError('Genre param must be '
                             'either string or Genre object')
        genre.save()

    def delete_genre(self, genre):
        if isinstance(genre, int):
            try:
                genre = Genre.objects.get(pk=genre)
            except Genre.DoesNotExist as e:
                raise ValueError(e)
        elif isinstance(genre, str):
            try:
                genre = Genre.objects.get(name__icontains=genre)
            except Genre.DoesNotExist as e:
                raise ValueError(e)
        elif not isinstance(genre, Genre):
            raise ValueError('Genre param must be '
                             'either string, integer '
                             'or Genre object')
        genre.delete()

    def delete_user(self, user):
        if isinstance(user, int):
            try:
                user = User.objects.get(pk=user)
            except Genre.DoesNotExist as e:
                raise ValueError(e)
        elif isinstance(user, str):
            try:
                user = User.objects.get(username__iexact=user)
            except Genre.DoesNotExist as e:
                raise ValueError(e)
        elif not isinstance(user, User):
            raise ValueError('User param must be either '
                             'instance of string, integer '
                             'or Genre object')
        user.delete()

    def _check_drawing(self, drawing):
        if isinstance(drawing, int):
            try:
                drawing = Drawing.objects.get(pk=drawing)
            except Drawing.DoesNotExist as e:
                raise ValueError(e)
        elif isinstance(drawing, str):
            try:
                drawing = Drawing.objects.get(name__icontains=drawing)
            except Drawing.DoesNotExist as e:
                raise ValueError(e)
        elif not isinstance(drawing, Drawing):
            raise ValueError('Drawing param must be '
                             'either string, integer '
                             'or Drawing object')
        return drawing

    def hide_image(self, drawing):
        drawing = self._check_drawing(drawing)
        drawing.hide()

    def show_image(self, drawing):
        drawing = self._check_drawing(drawing)
        drawing.show()

    def _check_exhibition(self, exhibition):
        if isinstance(exhibition, int):
            try:
                exhibition = Exhibition.objects.get(pk=exhibition)
            except Exhibition.DoesNotExist as e:
                raise ValueError(e)
        elif isinstance(exhibition, str):
            try:
                exhibition = Exhibition.objects.get(name__icontains=exhibition)
            except Exhibition.DoesNotExist as e:
                raise ValueError(e)
        elif not isinstance(exhibition, Exhibition):
            raise ValueError('Exhibition param must be '
                             'either string, integer '
                             'or Exhibition object')
        return exhibition

    def approve_exhibition(self, exhibition):
        exhibition = self._check_exhibition(exhibition)
        exhibition.approve()

    def disapprove_exhibition(self, exhibition):
        exhibition = self._check_exhibition(exhibition)
        exhibition.disapprove()


class ArtistManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ARTIST)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ARTIST,
                                   password, **extra_fields)


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

    def get_drawings(self):
        return self.drawings

    def create_drawing(self, name, description, image, genres=[]):
        assert isinstance(name, str) and name
        assert isinstance(description, str) and description
        assert isinstance(image, InMemoryUploadedFile)
        assert isinstance(genres, QuerySet) and genres.model is Genre \
               or \
               isinstance(genres, list) and (
                   all(isinstance(genre, Genre) for genre in genres)
                   or
                   all(isinstance(genre, int) for genre in genres)
               )
        drawing = Drawing.objects.create(
            name=name,
            description=description,
            artist=self,
            image=image
        )
        length = len(genres)
        if all(isinstance(genre, Genre) for genre in genres):
            genres = (genre.id for genre in genres)
        bulk = []
        for num, id in zip(range(1, length + 1), genres):
            bulk.append(DrawingGenre(genre_id=id, priority=num))

        drawing.drawinggenre_set = bulk

        return drawing


class OrganizerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ORGANIZER)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ORGANIZER,
                                   password, **extra_fields)


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

    def create_exhibition(self, name, description,
                          publish_date, genres=[], drawings=[]):
        assert isinstance(name, str) and name
        assert isinstance(description, str) and description
        assert isinstance(publish_date, datetime.date)
        assert isinstance(genres, QuerySet) and genres.model is Genre \
               or \
               isinstance(genres, list) and (
                   all(isinstance(genre, Genre) for genre in genres)
                   or
                   all(isinstance(genre, int) for genre in genres)
               )
        assert isinstance(drawings, QuerySet) and drawings.model is Drawing \
               or \
               isinstance(drawings, list) and (
                   all(isinstance(drawing, Genre) for drawing in drawings)
                   or
                   all(isinstance(drawing, int) for drawing in drawings)
               )
        exhibition = Exhibition.objects.create(
            name=name,
            description=description,
            publish_date=publish_date,
            organizer=self
        )
        length = len(genres)
        if all(isinstance(genre, Genre) for genre in genres):
            genres = (genre.id for genre in genres)
        bulk = []
        for num, id in zip(range(1, length + 1), genres):
            bulk.append(ExhibitionGenre(genre_id=id, priority=num))

        exhibition.exhibitiongenre_set = bulk

        if all(isinstance(drawing, Drawing) for drawing in drawings):
            drawings = (drawing.id for drawing in drawings)

        exhibition.drawings = drawings
        return exhibition

    def get_exhibitions(self):
        return self.exhibitions


name_regex = re.compile(r'^[А-Яа-яA-Za-z\w\s\.\,]+$')


class Genre(models.Model):
    name = models.CharField('название', max_length=32,
        validators=[
            validators.RegexValidator(name_regex,
                                      _('Название должно содержать '
                                        'только буквы латинского или '
                                        'кириллического алфавита.'),
                                      'invalid'),
        ],
    )
    __str__ = lambda self: self.name

    def get_related_exhibitions_page_url(self):
        return '%s?genre=%d' % (reverse('exhibitions-index'), self.pk)

    def get_related_drawings_page_url(self):
        return '%s?genre=%d' % (reverse('drawings-index'), self.pk)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class DrawingWithCountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(Count('exhibition'))


class Drawing(models.Model):

    def hide(self, save=True):
        self._set_hidden(True, save)

    def show(self, save=True):
        self._set_hidden(False, save)

    def _set_hidden(self, hidden, save=True):
        self.hidden = hidden
        if save: self.save(update_fields='hidden')

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

    def approve(self, save=True):
        self._set_approved(True, save)

    def disapprove(self, save=True):
        self._set_approved(False, save)

    def _set_approved(self, approved, save=True):
        self.approved = approved
        if save: self.save(update_fields='approved')

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

    def add_drawing(self, drawing):
        assert isinstance(drawing, (int, Drawing))
        self.drawings.add(drawing)

    def remove_drawing(self, drawing):
        assert isinstance(drawing, (int, Drawing))
        self.drawings.remove(drawing)

    @classmethod
    def get_by_genre(cls, genre):
        return cls.objects.filter(genres=genre)


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

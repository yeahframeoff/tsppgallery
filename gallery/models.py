from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
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
        verbose_name = 'адміністратор'
        verbose_name_plural = 'адміністратори'

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
        verbose_name = 'організатор виставок'
        verbose_name_plural = 'організатори виставок'

    def get_absolute_url(self):
        return reverse('organizer-detail', args=[self.pk])

    def owns_exhibition(self, exhibition):
        if not isinstance(exhibition, Exhibition):
            return Exhibition.objects.filter(pk=exhibition, organizer=self.id).exists()
        else:
            return exhibition.organizer_id == self.id


class Genre(models.Model):
    name = models.CharField('назва', max_length=32)
    __str__ = lambda self: self.name

    def get_related_exhibitions_page_url(self):
        return '%s?genre=%d' % (reverse('exhibitions-index'), self.pk)

    def get_related_drawings_page_url(self):
        return '%s?genre=%d' % (reverse('drawings-index'), self.pk)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанри'


class DrawingWithCountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(Count('exhibition'))


class Drawing(models.Model):
    image = models.ImageField('зображення', upload_to='images/%Y/%m/')
    name = models.CharField('назва', max_length=32)
    description = models.TextField('детальний опис')
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
        verbose_name='жанри'
    )
    hidden = models.BooleanField('малюнок сховано', default=False)
    date_uploaded = models.DateTimeField('завантажено', auto_now=True)
    __str__ = lambda self: self.name

    objects = DrawingWithCountManager()

    def get_absolute_url(self):
        return reverse('drawing-detail',args=[self.pk])

    def get_related_exhibitions_page_url(self):
        return '%s?drawing=%d' % (reverse('exhibitions-index'), self.pk)

    class Meta:
        verbose_name = 'малюнок'
        verbose_name_plural = 'малюнки'



class Exhibition(models.Model):
    drawings = models.ManyToManyField(
        Drawing,
        related_name='exhibitions',
        related_query_name='exhibition',
    )
    organizer = models.ForeignKey(Organizer,
                                  verbose_name='організатор',
                                  related_name='exhibitions',
                                  related_query_name='exhibition')
    name = models.CharField('назва', max_length=32)
    publish_date = models.DateField('дата публікації', auto_now=True)
    approved = models.BooleanField('виставку перевірено', default=False)
    genres = models.ManyToManyField(
        Genre,
        verbose_name='жанри',
        through='ExhibitionGenre',
        through_fields=('exhibition', 'genre'),
        related_name='exhibitions',
        related_query_name='exhibition'
    )
    description = models.TextField('Детальний опис')

    def get_absolute_url(self):
        return reverse('exhibition-detail',args=[self.pk])

    def __str__(self):
        return '%d %s' % (self.pk, self.name)

    class Meta:
        verbose_name = 'виставка'
        verbose_name_plural = 'виставки'
        ordering = ('id',)


class DrawingGenre(models.Model):
    drawing = models.ForeignKey(Drawing)
    genre = models.ForeignKey(Genre, verbose_name='жанр')
    priority = models.PositiveIntegerField('приорітет')

    def __str__(self):
        return "%d: drawing:%d, num:%d, genre:%d" %\
               (self.pk, self.drawing_id, self.priority, self.genre_id)

    class Meta:
        unique_together = ('drawing', 'genre')
        ordering = ('drawing_id', 'priority')



class ExhibitionGenre(models.Model):
    exhibition = models.ForeignKey(Exhibition)
    genre = models.ForeignKey(Genre, verbose_name='жанр')
    priority = models.PositiveIntegerField('приорітет')

    def __str__(self):
        return "%d: xzibit:%d, num:%d, genre:%d" %\
               (self.pk, self.exhibition_id, self.priority, self.genre_id)

    class Meta:
        unique_together = ('exhibition', 'genre')
        ordering = ('exhibition_id', 'priority')

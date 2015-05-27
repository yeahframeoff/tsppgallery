from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .gauth import UserCreationForm
from .models import User
from django.http import \
    HttpResponseRedirect, HttpResponse, \
    HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .models import \
    Artist, Organizer, Drawing, Exhibition, \
    DrawingGenre, Genre, ExhibitionGenre

from django.views import generic as genericviews
import json


def parse_ids_list(ids_list_str):
    if not ids_list_str or len(ids_list_str.strip()) == 0:
        return []
    return [int(id) for id in ids_list_str.split(',')]


def parse_ordered_ids_list(ids_list_str):
    if not ids_list_str or len(ids_list_str.strip()) == 0:
        return []
    ids_list = ids_list_str.split(',')
    length = len(ids_list_str)
    ids_list = (int(id) for id in ids_list)
    ids_list = (
        (num, id) for num, id in
        zip(range(1, length + 1), ids_list)
    )
    return ids_list


def main(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect(user.get_absolute_url())
    else:
        return HttpResponseRedirect(reverse('login'))


def register(request):
    if not request.user.is_anonymous():
        logout(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return HttpResponseRedirect(reverse('mainpage'))
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)
        return login_required(view)


class ArtistDetailView(LoginRequiredMixin, genericviews.DetailView):
    template_name = 'artist.html'
    context_object_name = 'artist'
    queryset = Artist.objects.all()\
        .prefetch_related('drawings__genres')


class OrganizerDetailView(LoginRequiredMixin, genericviews.DetailView):
    model = Organizer
    template_name = 'organizer.html'
    context_object_name = 'org'


class DrawingDetailView(LoginRequiredMixin, genericviews.DetailView):
    model = Drawing
    template_name = 'drawing/view.html'
    context_object_name = 'drawing'


class DrawingForm(forms.ModelForm):
    class Meta:
        model = Drawing
        fields = ('name', 'image', 'description')

    def save(self, commit=True):
        drawing = super().save()
        exhibition_drawings_ids_list = parse_ordered_ids_list(self.exhibition_drawings_ids_list)
        bulk = []
        for num, id in exhibition_drawings_ids_list:
            bulk.append(DrawingGenre(genre_id=id, priority=num))
        drawing.drawinggenre_set = bulk
        return drawing


@user_passes_test(User.check_artist)
def create_drawing(request):
    if request.method == 'POST':
        form = DrawingForm(request.POST, request.FILES)
        form.instance.artist = Artist.objects.get(pk=request.user.pk)
        if form.is_valid():
            form.exhibition_drawings_ids_list = request.session.pop('drawing_genres_ids_list', '')
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = DrawingForm()
    return render(request, 'drawing/edit.html', {'form': form})


class DrawingEditView(LoginRequiredMixin, genericviews.UpdateView):
    model = Drawing
    template_name = 'drawing/edit.html'
    context_object_name = 'drawing'
    fields = ('image', 'name', 'description')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_artist:
            return HttpResponseForbidden('Only artists can edit drawings')
        drawing_id = int(kwargs.get('pk', 0))
        if drawing_id <= 0:
            return HttpResponseBadRequest('Bad drawing id')
        elif not request.user.owns_drawing(drawing_id):
            return HttpResponseForbidden('Artists can edit only their own drawings')
        else:
            return super().dispatch(request, args, kwargs)


@user_passes_test(User.check_artist)
@require_POST
def delete_drawing(request, pk):
    try:
        drawing = Drawing.objects.get(pk=pk)
        if not request.user.owns_drawing(drawing):
            return HttpResponseForbidden('Artists can delete '
                                         'only their own drawings')
        drawing.delete()
    except Drawing.DoesNotExist:
        pass
    redirect_url = request.GET.get('HTTP_REFERER') or \
                   reverse('artist-detail', args=[request.user.pk])
    return HttpResponseRedirect(redirect_url)


@user_passes_test(User.check_organizer)
@require_POST
def delete_exhibition(request, pk):
    try:
        xzibit = Exhibition.objects.get(pk=pk)
        if not request.user.owns_exhibition(xzibit):
            return HttpResponseForbidden('Organizers can delete '
                                         'only their own exhibitions')
        xzibit.delete()
    except Drawing.DoesNotExist:
        pass
    redirect_url = request.GET.get('HTTP_REFERER') or \
                   reverse('organizer-detail', args=[request.user.pk])
    return HttpResponseRedirect(redirect_url)


class ExhibitionsView(LoginRequiredMixin, genericviews.ListView):
    template_name = 'exhibition/index.html'
    context_object_name = 'exhibitions'

    def get_queryset(self):
        req = self.request
        qs = Exhibition.objects.all()
        drawing_id = int(req.GET.get('drawing', 0))
        if drawing_id:
            self.drawing_id = drawing_id
            qs = qs.filter(drawings=drawing_id)
        genre_id = req.GET.get('genre')
        if genre_id:
            genre_id = int(genre_id)
            if genre_id > 0:
                self.genre_id = genre_id
                qs = qs.filter(genres=genre_id)
            else:
                qs = qs.annotate(genres_count=Count('genres'))\
                    .filter(genres_count=0)
        condition = Q(approved=True) | Q(approved=False, organizer=req.user)
        return qs.filter(condition)\
            .select_related('organizer').prefetch_related('drawings__genres')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if hasattr(self, 'genre_id'):
            context['genre'] = Genre.objects.get(id=self.genre_id)
        if hasattr(self, 'drawing_id'):
            context['drawing'] = Drawing.objects.get(id=self.drawing_id)
        return context


class DrawingsView(LoginRequiredMixin, genericviews.ListView):
    template_name = 'drawing/index.html'
    context_object_name = 'drawings'

    def get_queryset(self):
        req = self.request
        qs = Drawing.objects.all()
        genre_id = req.GET.get('genre')
        if genre_id:
            genre_id = int(genre_id)
            if genre_id > 0:
                self.genre_id = genre_id
                qs = qs.filter(genres=genre_id)
            else:
                qs = qs.annotate(genres_count=Count('genres'))\
                    .filter(genres_count=0)

        condition = Q(hidden=False) | Q(hidden=True, artist=req.user)
        return qs.filter(condition)\
            .select_related('artist').prefetch_related('genres')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if hasattr(self, 'genre_id'):
            context['genre'] = Genre.objects.get(id=self.genre_id)
        return context


class ExhibitionDetailView(LoginRequiredMixin, genericviews.DetailView):
    model = Exhibition
    template_name = 'exhibition/view.html'
    context_object_name = 'xzibit'


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ('name', 'description')

    def save(self, commit=True):
        xzibit = super().save()
        exhibition_genres_ids_list = parse_ordered_ids_list(self.exhibition_genres_ids_list)
        exhibition_drawings_ids_list = parse_ids_list(self.exhibition_drawings_ids_list)
        bulk = []
        for num, id in exhibition_genres_ids_list:
            bulk.append(ExhibitionGenre(genre_id=id, priority=num))

        xzibit.exhibitiongenre_set = bulk
        xzibit.drawings = exhibition_drawings_ids_list
        return xzibit


@user_passes_test(User.check_organizer)
def create_exhibition_view(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        form.instance.organizer = Organizer.objects.get(pk=request.user.pk)
        if form.is_valid():
            form.exhibition_genres_ids_list = request.session.pop('exhibition_genres_ids_list', '')
            form.exhibition_drawings_ids_list = request.session.pop('exhibition_drawings_ids_list', '')
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = ExhibitionForm()
    return render(request, 'exhibition/edit.html', {'form': form})


class ExhibitionEditView(LoginRequiredMixin, genericviews.UpdateView):
    model = Exhibition
    template_name = 'exhibition/edit.html'
    context_object_name = 'xzibit'
    fields = ('name', 'description')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer:
            return HttpResponseForbidden('Only organizers can '
                                         'edit exhibitions')
        exhibition_id = int(kwargs.get('pk', 0))
        if exhibition_id <= 0:
            return HttpResponseBadRequest('Bad exhibition id')
        elif not request.user.owns_exhibition(exhibition_id):
            return HttpResponseForbidden('Organizers can edit '
                                         'only their own exhibitions')
        else:
            return super().dispatch(request, args, kwargs)


class ViewAjaxOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden("This is an ajax view, friend.")
        return super(ViewAjaxOnlyMixin, self)\
            .dispatch(request, *args, **kwargs)


class ViewReturnJsonMixin(object):
    def render(self, queryset):
        values = queryset.values(*self.fields_to_serialize)
        return json.dumps(list(values))

    def get(self, request, *args, **kwargs):
        query_args = getattr(self, 'query_args', [])
        query_args = dict(((key, kwargs[key]) for key in query_args))
        content = self.render(self.get_queryset(**query_args))
        return HttpResponse(
            content=content,
            content_type='application/json'
        )


class ViewAjaxGetMixin(LoginRequiredMixin, ViewAjaxOnlyMixin, ViewReturnJsonMixin):
    pass


class GenresView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name')
    model = Genre


class DrawingsAjaxListView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name', 'image', 'genres')
    queryset = Drawing.objects.filter(hidden=False).prefetch_related('genres');

    def render(self, queryset):
        values = [
            {
                'id': x.id,
                'name': x.name,
                'url': x.image.url,
                'genres' : [g.name for g in x.genres.all()]
            }
            for x in queryset
        ]
        return json.dumps(values)


class DrawingGenresListView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name')
    query_args = ('pk',)

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        return Drawing.objects.get(pk=pk).genres\
            .order_by('drawinggenre__priority').all();


class ExhibitionGenresListView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name')
    query_args = ('pk',)

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        return Exhibition.objects.get(pk=pk).genres\
            .order_by('exhibitiongenre__priority').all();


class ExhibitionDrawingsListView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name', 'image')
    query_args = ('pk',)

    def render(self, queryset):
        values = [
            {
                'id': x.id,
                'name': x.name,
                'url': x.image.url,
                'genres' : [g.name for g in x.genres.all()]
            }
            for x in queryset
        ]
        return json.dumps(values)

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        return Exhibition.objects.get(pk=pk)\
            .drawings.all().prefetch_related('genres');


@user_passes_test(User.check_artist)
def update_drawing_genres_order(request, drawing_id):
    if not request.user.owns_drawing(drawing_id):
        return HttpResponseForbidden('Artists can edit '
                                     'only their own drawings')
    ids_list = request.POST.get('ids_order', True)
    if ids_list is True:
        return HttpResponseBadRequest()
    ids_list = parse_ordered_ids_list(ids_list)
    bulk = []
    DrawingGenre.objects.filter(drawing_id=drawing_id).delete()
    for num, id in ids_list:
        bulk.append(DrawingGenre(genre_id=id, priority=num))
    Drawing.objects.get(pk=drawing_id).drawinggenre_set = bulk
    return JsonResponse({'success': True})


@user_passes_test(User.check_organizer)
def update_exhibition_genres_order(request, exhibition_id):
    if not request.user.owns_exhibition(exhibition_id):
        return HttpResponseForbidden('Organizers can edit '
                                     'only their own exhibitions')
    ids_list = request.POST.get('ids_order', True)
    if ids_list is True:
        return HttpResponseBadRequest()
    ids_list = parse_ordered_ids_list(ids_list)
    bulk = []
    ExhibitionGenre.objects.filter(exhibition_id=exhibition_id).delete()
    for num, id in ids_list:
        bulk.append(ExhibitionGenre(genre_id=id, priority=num))
    Exhibition.objects.get(pk=exhibition_id).exhibitiongenre_set = bulk
    return JsonResponse({'success': True})


@user_passes_test(User.check_artist)
def preupdate_drawing_genres_order(request):
    ids_list = request.POST.get('ids_order', None)
    request.session['drawing_genres_ids_list'] = ids_list
    return JsonResponse({'success': True})


@user_passes_test(User.check_organizer)
def preupdate_exhibition_genres_order(request):
    ids_list = request.POST.get('ids_order', None)
    request.session['exhibition_genres_ids_list'] = ids_list
    return JsonResponse({'success': True})


@user_passes_test(User.check_organizer)
def update_exhibition_drawings_list(request, exhibition_id):
    if not request.user.owns_exhibition(exhibition_id):
        return HttpResponseForbidden('Organizers can edit '
                                     'only their own exhibitions')
    ids_list = request.POST.get('ids_order', True)
    if ids_list is True:
        return HttpResponseBadRequest()
    ids_list = parse_ids_list(ids_list)
    Exhibition.objects.get(pk=exhibition_id).drawings = ids_list
    return JsonResponse({'success': True})


@user_passes_test(User.check_organizer)
def preupdate_exhibition_drawings_list(request):
    ids_list = request.POST.get('ids_order', None)
    request.session['exhibition_drawings_ids_list'] = ids_list
    return JsonResponse({'success': True})

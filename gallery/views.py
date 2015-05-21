from django import forms
from django.conf import settings
from django.shortcuts import render
from .gauth import UserCreationForm
from django.http import \
    HttpResponseRedirect, HttpResponse, Http404,\
    HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from .models import \
    Artist, Organizer, Drawing, Exhibition, \
    DrawingGenre, Genre, ExhibitionGenre

from django.views import generic as genericviews
import json


def main(request):
    return render(request, 'mainpage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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


class ArtistDetailView(genericviews.DetailView):
    template_name = 'artist.html'
    context_object_name = 'artist'
    queryset = Artist.objects.all()\
        .prefetch_related('drawings__genres')


class OrganizerDetailView(genericviews.DetailView):
    model = Organizer
    template_name = 'organizer.html'
    context_object_name = 'org'


class DrawingDetailView(genericviews.DetailView):
    model = Drawing
    template_name = 'drawing-view.html'
    context_object_name = 'drawing'


class DrawingForm(forms.ModelForm):
    class Meta:
        model = Drawing
        fields = ('name', 'image', 'description')

    def save(self, commit=True):
        instance = super().save()
        ids_list = self.ids_list.split(',')
        length = len(ids_list)
        ids_list = (int(id) for id in ids_list)
        ids_list = (
            (num, id) for num, id in
            zip(range(1, length + 1), ids_list)
        )
        bulk = []
        for num, id in ids_list:
            bulk.append(DrawingGenre(genre_id=id, priority=num))
        Drawing.objects.get(pk=instance.pk).drawinggenre_set = bulk
        return instance


def create_drawing_view(request):
    if request.method == 'POST':
        form = DrawingForm(request.POST, request.FILES)
        form.instance.artist = Artist.objects.get(pk=request.user.pk)
        if form.is_valid():
            form.ids_list = request.session.get('drawing_genres_ids_list', '')
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = DrawingForm()
    return render(request, 'drawing-edit.html', {'form': form})


class DrawingEditView(genericviews.UpdateView):
    model = Drawing
    template_name = 'drawing-edit.html'
    context_object_name = 'drawing'
    fields = ('image', 'name', 'description')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_artist:
            return HttpResponseForbidden('Only artists can edit drawings')
        elif int(kwargs.get('pk', 0)) <= 0:
            return HttpResponseBadRequest('Bad drawing id')
        elif not Artist(request.user).owns(int(kwargs.get('pk', 0))):
            return HttpResponseForbidden('Artists can edit their drawings only')
        else:
            return super().dispatch(request, args, kwargs)


class ExhibitionDetailView(genericviews.DetailView):
    model = Exhibition
    template_name = 'exhibition-view.html'
    context_object_name = 'xzibit'


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ('name', 'description')

    def save(self, commit=True):
        instance = super().save()
        ids_list = self.ids_list.split(',')
        length = len(ids_list)
        ids_list = (int(id) for id in ids_list)
        ids_list = (
            (num, id) for num, id in
            zip(range(1, length + 1), ids_list)
        )
        bulk = []
        for num, id in ids_list:
            bulk.append(ExhibitionGenre(genre_id=id, priority=num))
        Exhibition.objects.get(pk=instance.pk).exhibitiongenre_set = bulk
        return instance


def create_exhibition_view(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        form.instance.organizer = Organizer.objects.get(pk=request.user.pk)
        if form.is_valid():
            form.ids_list = request.session.get('exhibition_genres_ids_list', '')
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = ExhibitionForm()
    return render(request, 'exhibition-edit.html', {'form': form})


class ExhibitionEditView(genericviews.UpdateView):
    model = Exhibition
    template_name = 'exhibition-edit.html'
    context_object_name = 'xzibit'
    fields = ('name', 'description')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer:
            return HttpResponseForbidden('Only organizers can edit exhibitions')
        elif int(kwargs.get('pk', 0)) <= 0:
            return HttpResponseBadRequest('Bad exhibition id')
        elif not Organizer(request.user).owns(int(kwargs.get('pk', 0))):
            return HttpResponseForbidden('Organizers can edit their drawings only')
        else:
            return super().dispatch(request, args, kwargs)


class ViewAjaxOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
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


class ViewAjaxGetMixin(ViewAjaxOnlyMixin, ViewReturnJsonMixin):
    pass


class GenresView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name')
    model = Genre


class DrawingsView(ViewAjaxGetMixin, genericviews.ListView):
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


def update_drawing_genres_order(request, drawing_id):
    ids_list = request.POST.get('ids_order', None)
    if not ids_list:
        return HttpResponseBadRequest()
    ids_list = ids_list.split(',')
    length = len(ids_list)
    ids_list = (int(id) for id in ids_list)
    ids_list = (
        (num, id) for num, id in
        zip(range(1, length + 1), ids_list)
    )
    bulk = []
    DrawingGenre.objects.filter(drawing_id=drawing_id).delete()
    for num, id in ids_list:
        bulk.append(DrawingGenre(genre_id=id, priority=num))
    Drawing.objects.get(pk=drawing_id).drawinggenre_set = bulk
    return JsonResponse({'success': True})

def update_exhibition_genres_order(request, exhibition_id):
    ids_list = request.POST.get('ids_order', None)
    if not ids_list:
        return HttpResponseBadRequest()
    ids_list = ids_list.split(',')
    length = len(ids_list)
    ids_list = (int(id) for id in ids_list)
    ids_list = (
        (num, id) for num, id in
        zip(range(1, length + 1), ids_list)
    )
    bulk = []
    ExhibitionGenre.objects.filter(exhibition_id=exhibition_id).delete()
    for num, id in ids_list:
        bulk.append(ExhibitionGenre(genre_id=id, priority=num))
    Exhibition.objects.get(pk=exhibition_id).exhibitiongenre_set = bulk
    return JsonResponse({'success': True})

def preupdate_drawing_genres_order(request):
    ids_list = request.POST.get('ids_order', None)
    request.session['drawing_genres_ids_list'] = ids_list
    return JsonResponse({'success': True})

def preupdate_exhibition_genres_order(request):
    ids_list = request.POST.get('ids_order', None)
    request.session['exhibition_genres_ids_list'] = ids_list
    return JsonResponse({'success': True})

def update_exhibition_drawings_list(request, exhibition_id):
    ids_list = request.POST.get('ids_order', None)
    if not ids_list:
        return HttpResponseBadRequest()
    ids_list = [int(id) for id in ids_list.split(',')]
    Exhibition.objects.get(pk=exhibition_id).drawings = ids_list
    return JsonResponse({'success': True})

def preupdate_exhibition_drawings_list(request, exhibition_id):
    ids_list = request.POST.get('ids_order', None)
    request.session['exhibition_drawings_ids_list'] = ids_list
    return JsonResponse({'success': True})
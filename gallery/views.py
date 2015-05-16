from django.shortcuts import render
from .gauth import UserCreationForm
from django.http import \
    HttpResponseRedirect, HttpResponse, Http404,\
    HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from .models import Artist, Organizer, Drawing, Exhibition, DrawingGenre, Genre

from django.views import generic as genericviews
import json


def main(request):
    return render(request, 'mainpage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('mainpage'))
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class ArtistDetailView(genericviews.DetailView):
    model = Artist
    template_name = 'artist.html'
    context_object_name = 'artist'


class OrganizerDetailView(genericviews.DetailView):
    model = Organizer
    template_name = 'organizer.html'
    context_object_name = 'org'


class DrawingDetailView(genericviews.DetailView):
    model = Drawing
    template_name = 'image-view.html'
    context_object_name = 'drawing'


class DrawingEditView(genericviews.UpdateView):
    model = Drawing
    template_name = 'image-edit.html'
    context_object_name = 'drawing'
    fields = ('image', 'name', 'description')


class DrawingCreateView(genericviews.CreateView):
    model = Drawing
    template_name = 'image-edit.html'
    context_object_name = 'drawing'
    fields = ('image', 'name', 'description')


class ExhibitionDetailView(genericviews.DetailView):
    model = Exhibition
    template_name = 'exhibition-view.html'
    context_object_name = 'xzibit'


class ExhibitionCreateView(genericviews.CreateView):
    model = Exhibition
    template_name = 'exhibition-edit.html'
    context_object_name = 'xzibit'


class ExhibitionEditView(genericviews.UpdateView):
    model = Exhibition
    template_name = 'exhibition-edit.html'
    context_object_name = 'xzibit'
    fields = ('name', 'description')


class ViewAjaxOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
        return super(ViewAjaxOnlyMixin, self).dispatch(request, *args, **kwargs)


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

    def get_queryset(self, **kwargs):
        exclude = self.request.GET.get('exclude', None)
        qs = Genre.objects.all()
        if exclude:
            exclude = [int(val) for val in exclude.split(',')]
            qs = qs.exclude(id__in=exclude)
        return qs


class DrawingGenresListView(ViewAjaxGetMixin, genericviews.ListView):
    fields_to_serialize = ('id', 'name')
    query_args = ('pk',)

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        return Drawing.objects.get(pk=pk).genres.order_by('drawinggenre__priority').all();


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


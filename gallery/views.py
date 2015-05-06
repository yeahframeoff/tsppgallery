from django.shortcuts import render
from .gauth import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from .models import Artist, Organizer, Drawing, Exhibition

from django.views import generic as genericviews


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


class ExhibitionDetailView(genericviews.DetailView):
    model = Exhibition
    template_name = 'exhibition-view.html'
    context_object_name = 'xzibit'

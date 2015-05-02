from django.shortcuts import render
from .models import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

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

from .models import Genre

def processor(request):
    genres = Genre.objects.all()
    return {'genres': genres}
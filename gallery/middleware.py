from .models import User, Artist, Admin, Organizer

class UserProxySubstituteMiddleware:
    def process_request(self, request):
        user = request.user
        if not isinstance(user, User) or not user.is_authenticated():
            return
        if user.is_artist:
            user.__class__ = Artist
        elif user.is_organizer:
            user.__class__ = Organizer
        elif user.is_superuser:
            user.__class__ = Admin

from django.db import models
from .gauth import Role, User, UserManager


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ADMIN)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ADMIN, password, **extra_fields)


class Admin(User):
    objects = AdminManager()
    class Meta(User.Meta):
        proxy = True


class ArtistManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ARTIST)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ARTIST, password, **extra_fields)


class Artist(User):
    objects = ArtistManager()
    class Meta(User.Meta):
        proxy = True


class OrganizerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.ORGANIZER)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, Role.ORGANIZER, password, **extra_fields)


class Organizer(User):
    objects = OrganizerManager()
    class Meta(User.Meta):
        proxy = True

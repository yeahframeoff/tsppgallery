from .gauth import Role, User, UserManager
from django.db import models

def make_user_proxy(role):
    if role not in Role.ROLES_LIST:
        raise ValueError('role must be the one from Role.ROLES_LIST')
    class ProxyUserManager(UserManager):
        def get_queryset(self):
            return super(ProxyUserManager, self)\
                .get_queryset().filter(role=role)

    class TheProxy(User):
        objects = ProxyUserManager()
        class Meta(User.Meta):
            proxy = True
        def save(self, *args, **kwargs):
            self.role = role
            super(Admin, self).save(*args, **kwargs)
    return TheProxy


Admin = make_user_proxy(Role.ADMIN)
Artist = make_user_proxy(Role.ARTIST)
Organizer = make_user_proxy(Role.ORGANIZER)

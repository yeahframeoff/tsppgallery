from django import forms
from django.contrib.auth import forms as authforms
from django.core import validators
from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, PermissionsMixin, UserManager, \
    Permission, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.contrib.auth import get_user_model


class Role(models.CharField):

    ADMIN = 'AD'
    ARTIST = 'AR'
    ORGANIZER = 'OR'

    ROLES_FORM_LIST = (
        (ARTIST, 'Artist'),
        (ORGANIZER, 'Organizer')
    )

    ROLES_LIST = ROLES_FORM_LIST + ((ADMIN, 'Admin'),)

    def __init__(self, *args, **kwargs):
        upd = {
            'max_length':2,
            'choices': self.ROLES_LIST,
            'default': self.ARTIST,
            'verbose_name':_('roles'),
            'blank': True,
            'help_text':_('The role this user belongs to. A user will '
                          'get all permissions granted to this role'),
        }
        kwargs.update(upd)
        super(Role, self).__init__(*args, **kwargs)


class RolePermission(models.Model):
    permission = models.ForeignKey(Permission, verbose_name='role_perm')
    role = Role()


class ModelBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def _get_role_permissions(self, user_obj):
        return Permission.objects.filter(**{'role___role_perm': user_obj.role})

    def _get_permissions(self, user_obj, obj):
        """
        Returns the permissions of `user_obj` from `from_name`. `from_name` can
        be either "role" or "user" to return permissions from
        `_get_role_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
            return set()

        perm_cache_name = '_role_perm_cache'
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, '_get_role_permissions')(user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            setattr(user_obj, perm_cache_name, set("%s.%s" % (ct, name) for ct, name in perms))
        return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return self._get_permissions(user_obj, obj)

    def get_role_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings the user `user_obj` has from the
        role they belong.
        """
        return self._get_permissions(user_obj, obj)

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = self.get_user_permissions(user_obj)
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Role and Permission model using the ModelBackend.
    """
    @property
    def is_superuser(self):
        return self.role == Role.ADMIN
    role = Role()

    class Meta:
        abstract = True

    def get_user_permissions(self):
        return self.get_role_permissions(self)

    @property
    def user_permissions(self):
        return self.get_user_permissions()

    def get_role_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through its
        role. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_role_permissions"):
                permissions.update(backend.get_role_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return auth.models._user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return auth.models._user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return auth.models._user_has_module_perms(self, app_label)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password,
                     is_staff, role, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          role=role,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, role=Role.ARTIST, password=None, **extra_fields):
        if role == Role.ADMIN:
            raise ValueError(_('To create admin user create_superuser() instead.'))
        return self._create_user(username, email, password, False, role,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, Role.ADMIN,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model with specific validators. As long as it is impossible
    to override field in Django model, I had to define a brand new model class.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=20, unique=True,
        help_text=_('Required. 4-20 characters. Small letters, digits,'
                    'dot and underscore characters.'),
        validators=[
            validators.RegexValidator(r'^[A-Za-z0-9._]{4,20}$',
                                      _('Enter a valid username. '
                                        'This value may contain only small letters, digits, '
                                        'dot and underscore characters. '
                                        'From 4 up to 20 characters.'),
                                      'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True,
        validators=[
            validators.RegexValidator(r'^([А-Я][а-я]+)|([A-Z][a-z]+)$',
                                      _('Имя должно быть введено в одной раскладке '
                                        'и начинаться с заглавной буквы'),
                                      'invalid'),
        ],
    )
    last_name = models.CharField(_('last name'), max_length=30, blank=True,
        validators=[
            validators.RegexValidator(r'^([А-Я][а-я]+)|([A-Z][a-z]+)$',
                                      _('Фамилия должна быть введена в одной раскладке '
                                        'и начинаться с заглавной буквы'),
                                      'invalid'),
        ],
    )
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    photo = models.ImageField(_('User photo'), upload_to='userphotos', null=True)
    bio = models.TextField(_('Biography'), blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if not self.first_name or not self.last_name:
            full_name = '@' + self.username
        else:
            full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        if not self.first_name or not self.last_name:
            short_name = '@' + self.username
        else:
            short_name = "%.1s. %s" % (self.first_name, self.last_name)
        return short_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        raise NotImplementedError()

    full_name = property(get_full_name)

    @property
    def is_artist(self):
        return self.role == Role.ARTIST

    @staticmethod
    def check_artist(user):
        return user.is_authenticated() and user.is_artist

    @property
    def is_organizer(self):
        return self.role == Role.ORGANIZER

    @staticmethod
    def check_organizer(user):
        return user.is_authenticated() and user.is_organizer

    def owns_drawing(self, drawing):
        return False

    def owns_exhibition(self, exhibition):
        return False


class UserCreationForm(authforms.UserCreationForm):
    class Meta(authforms.UserCreationForm.Meta):
        model = User
        fields = ('username', 'role', 'photo', 'first_name', 'last_name', 'email')

    role = forms.TypedChoiceField(choices=Role.ROLES_FORM_LIST)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()



class UserChangeForm(authforms.UserChangeForm):
    class Meta(authforms.UserChangeForm.Meta):
        model = User

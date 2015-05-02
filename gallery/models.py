from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
                                        'dot and underscore characters.'),
                                      'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

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
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."

        short_name = "%.1s. %s" % (self.first_name, self.last_name)
        return short_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        raise NotImplementedError()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

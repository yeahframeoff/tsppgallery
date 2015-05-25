from django.contrib import admin
from django.contrib.auth.models import Group as AuthDefaultGroup
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin

from . import gauth
from . import models


admin.site.unregister(AuthDefaultGroup)

@admin.register(models.User)
class UserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('bio', 'photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'role', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = gauth.UserChangeForm
    add_form = gauth.UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = tuple()


class DrawingHasGenresInline(admin.StackedInline):
    model = models.Drawing.genres.through
    verbose_name = 'жанр'
    verbose_name_plural = 'жанри малюнка'


class ExhibitionHasGenresInline(admin.StackedInline):
    model = models.Exhibition.genres.through
    verbose_name = 'жанр'
    verbose_name_plural = 'жанри виставки'



class ExhibitionHasDrawingsInline(admin.StackedInline):
    model = models.Exhibition.drawings.through
    verbose_name = 'малюнки'
    verbose_name_plural = 'малюнки цієї виставки'


@admin.register(models.Drawing)
class DrawingAdmin(admin.ModelAdmin):
    inlines = (DrawingHasGenresInline,)
    fields = ('name', 'description', 'artist', 'image', 'hidden')
    save_as = True
    save_on_top = True


@admin.register(models.Exhibition)
class Exhibition(admin.ModelAdmin):
    fields = ('name', 'organizer', 'approved','description')
    inlines = (ExhibitionHasGenresInline, ExhibitionHasDrawingsInline)


admin.site.register(models.Genre)
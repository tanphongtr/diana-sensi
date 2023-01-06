from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from app.models import User
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ImportExportActionModelAdmin, ImportMixin
from django.utils.translation import gettext_lazy as _


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(ImportExportActionModelAdmin, UserAdmin):
    form = MyUserChangeForm
    actions = []
    actions_on_bottom = True
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'full_address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(User, MyUserAdmin)

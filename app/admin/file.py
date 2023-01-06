from django.contrib import admin
from app.models import File
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.safestring import mark_safe


__all__ = ['FileAdmin']

# from django_api.views import file_downloading


class FilterWithCustomTemplate(admin.DateFieldListFilter):
    template = "custom_template.html"


@admin.register(File)
class FileAdmin(admin.ModelAdmin):

    list_display = ('id', 'file', 'created_at', )
    search_fields = ['created_at']
    # filter=['sid']
    # list_filter=['sid']
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateRangeFilter),

    )

    fields = ('file', 'headshot_image', )
    readonly_fields = ('headshot_image', )

    def headshot_image(self, obj):
        return mark_safe('<img src="{url}" />'.format(
            url=obj.file.url,
        ))

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    # pass

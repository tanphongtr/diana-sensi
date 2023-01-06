from django.contrib import admin
from app.models import Market
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


# from django_api.views import file_downloading

class MarketAdmin(admin.ModelAdmin):

    list_display = ('id', 'index', 'name', 'system', )
    search_fields = ['name']
    list_display_links = ('name', )

    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .select_related('system')\
            .prefetch_related('system__province')\
            # .prefetch_related('')

admin.site.register(Market, MarketAdmin)

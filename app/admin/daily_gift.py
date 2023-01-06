from django.contrib import admin
from app.models import DailyGift
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


# from django_api.views import file_downloading

class DailyGiftAdmin(admin.ModelAdmin):

    list_display = ('pg_name', 'pg_phone_number', 'gift_name', 'quantity', 'remaining', 'date')
    search_fields = ['pg_phone_number']
    list_display_links = ('pg_name', )

    list_filter = (
        'pg_phone_number',
        'created_at',
    )


    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

    def get_queryset(self, request):
        queryset = super().get_queryset(request).\
            select_related('gift')
        return queryset

    def gift_name(self, obj):
        return obj.gift.name

admin.site.register(DailyGift, DailyGiftAdmin)

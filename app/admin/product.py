from django.contrib import admin
from app.models import Product
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


# from django_api.views import file_downloading

class ProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'index', 'name', 'price', )
    search_fields = ['name']
    list_display_links = ('name', )

    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

admin.site.register(Product, ProductAdmin)

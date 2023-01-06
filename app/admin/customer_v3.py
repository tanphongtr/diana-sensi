from django.contrib import admin, messages
from app.models import Customer, Survey, Invoice, InvoiceProduct, InvoiceGift, SurveyQuestion, SurveyAnswer
from app.models.customer import CustomerV3
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
import nested_admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ImportExportActionModelAdmin, ImportMixin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django import forms
from django.utils.safestring import mark_safe
import os
from .customer_serializers_v2 import CustomerSerializer
import datetime
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q


@admin.register(CustomerV3)
class CustomerV2Admin(nested_admin.NestedModelAdmin,):

    list_display = ('_invoice_photo', )

    list_filter = (
        ('created_at', DateRangeFilter),
        'market__name',
        'invoices__products__product__name',
        'invoices__gifts__gift__name',
        'created_at',
        'pg_phone_number',
    )

    list_max_show_all = 10
    list_per_page = 10

    def _invoice_photo(self, obj):
        return format_html(
            '<img src="{}" style="width:100%; height:auto;" />'.format(obj.invoice_photo.url)
        )

    def has_change_permission(self, request, obj=None):
        return True if request.user.username in ['admin', 'root'] else False

    def has_add_permission(self, request, obj=None):
        return True if request.user.username in ['admin', 'root'] else False

    def has_delete_permission(self, request, obj=None):
        return False if request.user.username in ['admin', 'root'] else False

    def has_view_permission(self, request, obj=None):
        return True

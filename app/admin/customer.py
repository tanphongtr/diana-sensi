from django.contrib import admin, messages
from app.models import Customer, Survey, Invoice, InvoiceProduct, InvoiceGift, SurveyQuestion, SurveyAnswer
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
import nested_admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ImportExportActionModelAdmin, ImportMixin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django import forms
from django.utils.safestring import mark_safe
import os
from .customer_serializers import CustomerSerializer
import datetime
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        answers = cleaned_data.get('answers')
        question = cleaned_data.get('question')

        if answers.count() > question.limit_answer and question.limit_answer > 0:
            raise forms.ValidationError(f"You can't assign more than {question.limit_answer} answers")

        return cleaned_data


class SurveyInline(nested_admin.NestedTabularInline):
    model = Survey
    extra = 0
    form = SurveyForm

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

class InvoiceProductInline(nested_admin.NestedTabularInline):
    model = InvoiceProduct
    extra = 0

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

class InvoiceGiftInline(nested_admin.NestedTabularInline):
    model = InvoiceGift
    extra = 0

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        print(cleaned_data)

        return cleaned_data

class InvoiceInline(nested_admin.NestedTabularInline):
    model = Invoice
    inlines = [
        InvoiceProductInline,
        InvoiceGiftInline,
    ]

    extra = 0

    form = InvoiceForm

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


def handle_export(data):
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(data)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f'/diana_sensi_export_data_{time}.xlsx'
    writer = pd.ExcelWriter(
        str(settings.MEDIA_ROOT) + file_name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.index += 1
    df.to_excel(writer, sheet_name='Sheet1', startrow=3)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    header_cell_format = workbook.add_format({
        'bold': True,
        'bottom': 6,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

    worksheet.merge_range('A1:Z1', 'CUSTOMER DATA', header_cell_format)
    worksheet.merge_range('A2:A4', 'NO.', header_cell_format)
    worksheet.merge_range('B2:B4', 'WEEK', header_cell_format)

    worksheet.merge_range('C2:C4', 'WORKING DAY', header_cell_format)
    worksheet.merge_range('D2:D4', 'PROVINCE', header_cell_format)
    worksheet.merge_range('E2:E4', 'TYPE', header_cell_format)
    worksheet.merge_range('F2:F4', 'SUPERMARKET', header_cell_format)
    worksheet.merge_range('G2:G4', 'CUSTOMER NAME', header_cell_format)
    worksheet.merge_range('H2:H4', 'PHONE NUMER', header_cell_format)

    worksheet.merge_range('I2:N3', 'SALE', header_cell_format)
    worksheet.write(3, 8, 'Diana Sensi 8M', header_cell_format)
    worksheet.write(3, 9, 'Diana Sensi 20M', header_cell_format)
    worksheet.write(3, 10, 'Mặt bông khác', header_cell_format)
    worksheet.write(3, 11, 'Mặt lưới khác', header_cell_format)
    worksheet.write(3, 12, 'Khác', header_cell_format)
    worksheet.write(3, 13, 'TOTAL', header_cell_format)
    worksheet.write(3, 14, 'Diana Sensi 8M', header_cell_format)
    worksheet.merge_range('O2:O4', 'REVENUE', header_cell_format)

    worksheet.merge_range('P2:U2', 'GIFT', header_cell_format)
    worksheet.write(2, 15, 'BILL 59K', header_cell_format)
    worksheet.merge_range('Q3:R3', 'BILL 79K', header_cell_format)
    worksheet.merge_range('S3:U3', 'BILL 129K', header_cell_format)

    worksheet.write(3, 15, 'Đồng hồ', header_cell_format)
    worksheet.write(3, 16, 'Ly thuỷ tinh', header_cell_format)
    worksheet.write(3, 17, 'Bấm móng tay', header_cell_format)
    worksheet.write(3, 18, 'Túi tote', header_cell_format)
    worksheet.write(3, 19, 'Máy duỗi tóc', header_cell_format)
    worksheet.write(3, 20, 'Gấu bông', header_cell_format)
    worksheet.merge_range('V2:V4', 'TOTAL BILL', header_cell_format)

    worksheet.merge_range('W2:W4', 'MÃ HOÁ ĐƠN', header_cell_format)
    worksheet.merge_range('X2:X4', 'LINK HOÁ ĐƠN', header_cell_format)

    worksheet.merge_range('Y2:Z2', 'SURVEY', header_cell_format)
    worksheet.merge_range('Y3:Y4', 'Đã từng sử dụng Diana Sensi chưa', header_cell_format)
    worksheet.merge_range('Z3:Z4', 'Tại sao chọn mua sp Diana Sensi', header_cell_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    return redirect(str(settings.MEDIA_URL) + file_name)

def export(modeladmin, request, queryset):
    queryset = queryset.select_related('market', 'market__system__province', )\
        .prefetch_related('invoices')\
        .prefetch_related('invoices__products')\
        .prefetch_related('invoices__products__product')\
        .prefetch_related('invoices__gifts')\
        .prefetch_related('invoices__gifts__gift')\
        .prefetch_related('surveys')\
        .prefetch_related('surveys__question')\
        .prefetch_related('surveys__answers')

    serializer = CustomerSerializer(queryset, many=True)

    # print(serializer.data)
    return handle_export(serializer.data)

@admin.register(Customer)
class CustomerAdmin(nested_admin.NestedModelAdmin,):

    list_display = ('id', 'market', 'pg_name', 'pg_phone_number', 'name', 'phone_number', 'products', 'gifts', 'invoice_total', 'invoice_code', 'created_at')

    search_fields = ['name', '^phone_number', 'pg_name', '^pg_phone_number', '^invoices__code',]
    # list_display_links = ('customer_name', )

    inlines = [
        SurveyInline,
        InvoiceInline,
    ]

    form = CustomerForm
    fields = ('name', 'phone_number', 'pg_name', 'pg_phone_number', 'invoice_photo', '_invoice_photo', 'market' )
    readonly_fields = ('_invoice_photo',)

    list_filter = (
        ('created_at', DateRangeFilter),
        'market__name',
        'pg_phone_number',
        'invoices__products__product__name',
        'invoices__gifts__gift__name',
        'created_at',
        
    )

    list_max_show_all = 50
    list_per_page = 20

    # def has_change_permission(self, request, obj=None):
    #     return True

    def invoice_total(self, obj):
        if obj.invoices.count() > 0:
            return int(obj.invoices.first().total)
        return 0

    def products(self, obj):
        _product = ''
        invoices = obj.invoices.first()

        if not invoices:
            return _product

        products = invoices.products.all()
        _product = ''
        for product in products:
            _product += f'{product.product.name} ({product.quantity})<br />'

        return format_html(_product)

    def gifts(self, obj):
        _gift = ''
        invoices = obj.invoices.first()

        if not invoices:
            return _gift

        gifts = invoices.gifts.all()
        _gift = ''
        for gift in gifts:
            _gift += f'{gift.gift.name} ({gift.quantity})<br />'

        return format_html(_gift)

    def has_delete_permission(self, request, obj=None):
        return True

    def _invoice_photo(self, obj):
        return mark_safe('<img src="{url}" width="60%" />'.format(
            url=obj.invoice_photo.url,
        ))


    def invoice_code(self, obj):
        invoice = obj.invoices.first()
        if not invoice:
            return ''
        return invoice.code

    actions = [export]

    def get_queryset(self, request):
        qs = super().get_queryset(request)\
            .prefetch_related('invoices')\
            .prefetch_related('invoices__products')\
            .prefetch_related('invoices__products__product')\
            .prefetch_related('invoices__gifts')\
            .prefetch_related('invoices__gifts__gift')
        return qs


    def get_changelist(self, request, **kwargs):
        """
        Return the ChangeList class for use on the changelist page.
        """
        from django.contrib.admin.views.main import ChangeList

        class MyChangeList(ChangeList):
            def get_queryset(self, request):
                return super().get_queryset(request).filter(created_at__lte='2022-10-26 23:59:59')

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                from django.db.models import Sum, Count
                from django.db.models.functions import Coalesce
                from app.models import Product, Gift
                from app.models.common import TypeTextChoices


                model_list = self.queryset
                self.total_data = model_list.all().count()
                self.revenue = int(model_list.all().aggregate(total=Coalesce(Sum('invoices__total'), 0))['total'])
                self.gift_total = model_list.all().aggregate(total=Coalesce(Sum('invoices__gifts__quantity'), 0))['total']
                
                self.DONG_HO_DEO_TAY = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.DONG_HO_DEO_TAY)), 0))['total']

                self.LY_THUY_TINH = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.LY_THUY_TINH)), 0))['total']
                
                self.HOP_BAM_MONG_TAY = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.HOP_BAM_MONG_TAY)), 0))['total']

                self.TUI_TOTE = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.TUI_TOTE)), 0))['total']

                self.MAY_LA_TOC = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.MAY_LA_TOC)), 0))['total']

                self.UNICORN_KHONG_LO = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__gifts__quantity',
                    filter=Q(invoices__gifts__gift__code=Gift.CodeChoices.UNICORN_KHONG_LO)), 0))['total']

                self.SENSI_8M = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__products__quantity',
                    filter=Q(invoices__products__product__code=Product.CodeChoices.SENSI_8M)), 0))['total']

                self.SENSI_20M = model_list.all().aggregate(total=Coalesce(
                    Sum('invoices__products__quantity',
                    filter=Q(invoices__products__product__code=Product.CodeChoices.SENSI_20M)), 0))['total']

                self.GIFT_BILL_59K = self.DONG_HO_DEO_TAY

                self.GIFT_BILL_79K = int(self.LY_THUY_TINH) + int(self.HOP_BAM_MONG_TAY)
                
                self.GIFT_BILL_129K = int(self.UNICORN_KHONG_LO) + int(self.TUI_TOTE) + int(self.MAY_LA_TOC)

        return MyChangeList

    change_list_template = "Homepage.html"
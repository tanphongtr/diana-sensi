from rest_framework import serializers
from app.models import Customer, Gift


class CustomerSerializer(serializers.ModelSerializer):

    week = serializers.CharField(default='')
    working_day = serializers.DateTimeField(
        format="%d/%m/%Y", source='created_at',)
    province = serializers.CharField(source='market.system.province.name',)
    type = serializers.CharField(default='')
    super_market = serializers.CharField(source='market.name',)
    customer_name = serializers.CharField(source='name',)
    phone_number = serializers.CharField()

    # sale
    _diana_sensi_8m = serializers.SerializerMethodField()
    _diana_sensi_20m = serializers.SerializerMethodField()
    _mat_bong_khac = serializers.SerializerMethodField()
    _mat_luoi_khac = serializers.SerializerMethodField()
    _khac = serializers.SerializerMethodField()
    _total = serializers.SerializerMethodField()

    revenue = serializers.SerializerMethodField()

    # gift
    _bam_mong_tay = serializers.SerializerMethodField()
    _dong_ho = serializers.SerializerMethodField()
    _ly_thuy_tinh = serializers.SerializerMethodField()
    _dong_ho = serializers.SerializerMethodField()
    
    _tui_tote = serializers.SerializerMethodField()
    _may_duoi_toc = serializers.SerializerMethodField()
    _gau_bong = serializers.SerializerMethodField()
    _total_of_bill = serializers.SerializerMethodField()

    _ma_hoa_don = serializers.SerializerMethodField()
    invoice_photo = serializers.ImageField(use_url=True)

    # survey
    _CAU_HOI_1 = serializers.SerializerMethodField()
    _CAU_HOI_2 = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'week',
            'working_day',
            'province',
            'type',
            'super_market',
            'customer_name',
            'phone_number',
            '_diana_sensi_8m',
            '_diana_sensi_20m',
            '_mat_bong_khac',
            '_mat_luoi_khac',
            '_khac',
            '_total',
            'revenue',
            '_bam_mong_tay',
            '_ly_thuy_tinh',
            '_dong_ho',
            '_tui_tote',
            '_may_duoi_toc',
            '_gau_bong',
            '_total_of_bill',
            '_ma_hoa_don',
            'invoice_photo',
            '_CAU_HOI_1',
            '_CAU_HOI_2',
        ]

    def get__diana_sensi_8m(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()
            for invoice_product in invoice_products:
                if invoice_product.product.code == 'SENSI_8M':
                    return invoice_product.quantity
        return 0

    def get__diana_sensi_20m(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()
            for invoice_product in invoice_products:
                if invoice_product.product.code == 'SENSI_20M':
                    return invoice_product.quantity
        return 0

    def get__mat_bong_khac(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()
            for invoice_product in invoice_products:
                if invoice_product.product.code == 'MAT_BONG_KHAC':
                    return invoice_product.quantity
        return 0

    def get__mat_luoi_khac(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()
            for invoice_product in invoice_products:
                if invoice_product.product.code == 'MAT_LUOI_KHAC':
                    return invoice_product.quantity
        return 0

    def get__khac(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()
            for invoice_product in invoice_products:
                if invoice_product.product.code == 'KHAC':
                    return invoice_product.quantity
        return 0

    def get__total(self, obj):
        total = 0
        invoice = obj.invoices.all()

        if len(invoice):
            invoice = invoice[0]
            invoice_products = invoice.products.all()

            for invoice_product in invoice_products:
                total += invoice_product.quantity

        return total

    def get_revenue(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            return int(invoice.total)
        return 0

    def get__dong_ho(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.DONG_HO_DEO_TAY:
                    return invoice_gift.quantity
        return 0

    def get__ly_thuy_tinh(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.LY_THUY_TINH:
                    return invoice_gift.quantity
        return 0

    def get__bam_mong_tay(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.HOP_BAM_MONG_TAY:
                    return invoice_gift.quantity
        return 0

    def get__tui_tote(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.TUI_TOTE:
                    return invoice_gift.quantity
        return 0
    def get__may_duoi_toc(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.MAY_LA_TOC:
                    return invoice_gift.quantity
        return 0

    def get__gau_bong(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            invoice_gifts = invoice.gifts.all()
            for invoice_gift in invoice_gifts:
                if invoice_gift.gift.code == Gift.CodeChoices.UNICORN_KHONG_LO:
                    return invoice_gift.quantity
        return 0

    def get__total_of_bill(self, obj):
        return self.get__dong_ho(obj=obj) \
            + self.get__ly_thuy_tinh(obj=obj) \
            + self.get__bam_mong_tay(obj=obj) \
            + self.get__tui_tote(obj=obj) \
            + self.get__may_duoi_toc(obj=obj) \
            + self.get__gau_bong(obj=obj)

    def get__ma_hoa_don(self, obj):
        invoice = obj.invoices.all()
        if len(invoice):
            invoice = invoice[0]
            return invoice.code
        return None

    def get__CAU_HOI_1(self, obj):
        surveys = obj.surveys.all()
        for survey in surveys:
            if survey.question.code == 'CAU_1':
                return survey.answers.all()[0].answer
        return None

    def get__CAU_HOI_2(self, obj):
        surveys = obj.surveys.all()
        for survey in surveys:
            if survey.question.code == 'CAU_2':
                return survey.answers.all()[0].answer
        return None
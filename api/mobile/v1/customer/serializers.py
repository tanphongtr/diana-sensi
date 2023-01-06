from rest_framework import serializers
from app.models import (
    DailyGift, Customer, Invoice, InvoiceGift, InvoiceProduct, Survey, SurveyAnswer, SurveyQuestion)
from django.utils import timezone
from django.db import transaction

class InvoiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProduct
        fields = ('product', 'quantity', )


class InvoiceGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceGift
        fields = ('gift', 'quantity', )


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_products = InvoiceProductSerializer(many=True, )
    invoice_gifts = InvoiceGiftSerializer(many=True, )

    class Meta:
        model = Invoice
        fields = ('invoice_products', 'invoice_gifts', 'total', 'code')


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('question', 'answers', )


class CustomerSerializer(serializers.ModelSerializer):

    invoice = InvoiceSerializer(many=False, write_only=True, )
    surveys = SurveySerializer(many=True, write_only=True, )
    _invoice_photo = serializers.CharField(write_only=True, help_text='Lấy file_name từ API /api/mobile/v1/file/')

    class Meta:
        model = Customer
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        _invoice_photo = validated_data.pop('_invoice_photo')
        invoice_data = validated_data.pop('invoice')
        invoice_products = invoice_data.pop('invoice_products')
        invoice_gifts = invoice_data.pop('invoice_gifts')


        surveys_data = validated_data.pop('surveys')

        customer = Customer.objects.create(invoice_photo=_invoice_photo, **validated_data)

        invoice = self.__create_invoice(customer, invoice_data)
        self.__create_invoice_products( invoice, invoice_products)
        self.__create_invoice_gifts(validated_data['pg_phone_number'], invoice, invoice_gifts)
        self.__create_surveys(customer, surveys_data)

        
        return customer

    def __create_invoice(self, customer, invoice_data):
        invoice = Invoice.objects.create(customer=customer, **invoice_data)
        return invoice

    def __create_invoice_products(self, invoice, invoice_products):

        for invoice_product in invoice_products:
            product = invoice_product.pop('product')
            quantity = invoice_product.pop('quantity')
            price = product.price
            total = quantity * price

            InvoiceProduct.objects.create(
                product=product,
                invoice=invoice,
                quantity=quantity,
                price=price,
                total=total,
            )


    def __create_invoice_gifts(self, pg_phone_number, invoice, invoice_gifts):
        daily_gifts = DailyGift.objects.filter(
            pg_phone_number=pg_phone_number,
            date=timezone.now().date(),
        )

        for invoice_gift in invoice_gifts:
            gift = invoice_gift.pop('gift')
            quantity = invoice_gift.pop('quantity')
            value = gift.value
            total = quantity * value

            InvoiceGift.objects.create(
                gift=gift,
                invoice=invoice,
                quantity=quantity,
                value=value,
                total=total,
            )

            print("created invoice gift", daily_gifts), 

            for daily_gift in daily_gifts:
                print('----', daily_gift.gift.name, gift.name)
                if daily_gift.gift == gift:
                    print('======', daily_gift.gift.name, gift.name)
                    daily_gift.remaining = daily_gift.remaining - quantity if (daily_gift.remaining - quantity) > 0 else 0
                    daily_gift.save()

    def __create_surveys(self, customer, surveys_data):
        for survey_data in surveys_data:
            question = survey_data.pop('question')
            answers = survey_data.pop('answers', [])
            other_answer = survey_data.pop('other_answer', None)

            survey = Survey.objects.create(
                customer=customer, question=question, other_answer=other_answer)
            for answer in answers:
                if answer.question != question:
                    raise serializers.ValidationError(
                        'Answer does not belong to question')
            survey.answers.add(*answers)


    def __update_daily_gift(self, pg_phone_number, invoice_gifts):
        daily_gifts = DailyGift.objects.filter(
            pg_phone_number=pg_phone_number,
            date=timezone.now().date(),
        )

        for daily_gift in daily_gifts:
            pass
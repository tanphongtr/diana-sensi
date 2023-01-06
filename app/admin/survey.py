from django.contrib import admin
from django import forms
from app.models import SurveyQuestion, SurveyAnswer, Survey
from django.utils.html import format_html
from django.urls import path
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        answers = cleaned_data.get('answers')
        invoices = cleaned_data.get('invoices')
        question = cleaned_data.get('question')

        if question.limit_answer > 0 and len(answers) > question.limit_answer:
            raise forms.ValidationError(
                "You can select only %s answers" % question.limit_answer
            )

        if len(invoices) > 1:
            raise forms.ValidationError(
                "You can select only one invoice"
            )

        return cleaned_data



class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer

class SurveyQuestionAdmin(admin.ModelAdmin):

    list_display = ('id', 'index','question', )
    list_display_links = ('question', )
    search_fields = ['sid', 'question']
    inlines = [
        SurveyAnswerInline,
    ]

    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

class SurveyAnswerAdmin(admin.ModelAdmin):

    list_display = ('id', 'index', 'answer',)
    search_fields = ['sid', 'answer']
    list_display_links = ('answer', )

    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

# admin.site.register(SurveyAnswer, SurveyAnswerAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)



class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    # model = Survey
    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True

    def get_queryset(self, request):
        return super().get_queryset(request).\
            select_related('customer', 'question')

admin.site.register(Survey, SurveyAdmin)
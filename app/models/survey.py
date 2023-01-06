from django.db import models
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey, ChainedManyToManyField


class SurveyQuestion(models.Model):
    question = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, default=None, )
    limit_answer = models.IntegerField(default=0, blank=True, null=True)
    index = models.IntegerField(default=0)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.question or self.code

    class Meta:
        verbose_name = 'Survey Question'
        verbose_name_plural = 'Survey Questions'
        ordering = ['index', ]
        db_table = 'survey_question'


class SurveyAnswer(models.Model):
    question = models.ForeignKey("app.SurveyQuestion", on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, default=None, )
    index = models.IntegerField(default=0)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.answer or self.code

    class Meta:
        verbose_name = 'Survey Answer'
        verbose_name_plural = 'Survey Answers'
        ordering = ['index', ]
        db_table = 'survey_answer'


class Survey(models.Model):

    question = models.ForeignKey("app.SurveyQuestion", on_delete=models.PROTECT)
    # answers = models.ManyToManyField("app.SurveyAnswer", blank=True, )
    answers = ChainedManyToManyField(
        "app.SurveyAnswer",
        chained_field="question",
        chained_model_field="question",
        verbose_name="Answers",
        blank=True,
        null=True,
        help_text="Select answers",
    )
    other_answer = models.CharField(max_length=255, blank=True, null=True, default=None,)
    customer = models.ForeignKey("app.Customer", on_delete=models.CASCADE, related_name='surveys', )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        unique_together = (('customer', 'question'),)
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
        ordering = ['question__index', ]
        db_table = 'survey'

    # def clean(self, *args, **kwargs):
    #     if self.answers.count() > 3:
    #         raise ValidationError("You can't assign more than three regions")
    #     super().clean(*args, **kwargs)

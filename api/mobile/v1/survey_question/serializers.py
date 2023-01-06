from rest_framework import serializers
from app.models import SurveyQuestion, SurveyAnswer


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = '__all__'


class SurveyQuestionSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = '__all__'

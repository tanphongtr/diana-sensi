from rest_framework import generics
from .serializers import SurveyQuestionSerializer
from app.models import SurveyQuestion
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.common.paginations import StandardResultsSetPagination


swagger_tags = ['SurveyQuestion']


class SurveyQuestionAPIView(generics.ListAPIView):
    serializer_class = SurveyQuestionSerializer
    queryset = SurveyQuestion.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000

    def get_queryset(self):
        return SurveyQuestion.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List SurveyQuestions',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
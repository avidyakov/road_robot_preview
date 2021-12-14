from rest_framework import generics, filters

from .models import Question
from .serializers import QuestionSerializer


class QuestionSearch(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('question', )

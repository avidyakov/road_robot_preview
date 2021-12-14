from rest_framework.serializers import ModelSerializer

from .models import Question


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question', 'answer', 'hint', 'image_url')

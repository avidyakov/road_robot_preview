from django.db import models


class Question(models.Model):
    question = models.CharField('Вопрос', max_length=511)
    answer = models.CharField('Ответ', max_length=511)
    hint = models.TextField('Подсказка')
    image_origin = models.URLField('URL изображения')
    file_id = models.CharField('File id телеграм', max_length=255, null=True, blank=True)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='questions')

    def image_url(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

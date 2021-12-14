from django.db import models


class User(models.Model):
    username = models.CharField('Юзернейм', max_length=127, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=127, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=127, blank=True, null=True)
    chosen_query_count = models.IntegerField('Количество выбранных вопросов', default=0)
    payment = models.BooleanField('Оплата', default=False)

    def access(self):
        if self.chosen_query_count < 3:
            return True

        return self.payment

    def __str__(self):
        return self.username or str(self.id)

    class Meta:
        verbose_name = 'Пользователь телеграм'
        verbose_name_plural = 'Пользователи телеграм'

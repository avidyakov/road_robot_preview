from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages


from .models import Question


class QuestionResource(resources.ModelResource):

    class Meta:
        model = Question


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    actions = ('set_file_id', 'save_image_by_url')

    @admin.action(description='Установить телеграм file_id')
    def set_file_id(self, request, queryset):
        from .actors import set_file_id

        for question in queryset:
            set_file_id.send(question.id)

        number_of_questions = queryset.count()
        self.message_user(request, f'Поставили в очередь {number_of_questions} шт.', messages.SUCCESS)

    @admin.action(description='Сохранить изображение по ссылке')
    def save_image_by_url(self, request, queryset):
        from .actors import save_image_by_url

        for question in queryset:
            save_image_by_url.send(question.id)

        number_of_questions = queryset.count()
        self.message_user(request, f'Поставили в очередь {number_of_questions} шт.', messages.SUCCESS)

from django.contrib import admin
from django.core.exceptions import ValidationError
from teacher.models import Teacher, Subject
from django import forms


class TeacherForm(forms.ModelForm):
    model = Teacher

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subjects').count() > 5:
            raise ValidationError(
                'You have to choose exactly 5 subjects for each teacher')


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    pass


class SubjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)

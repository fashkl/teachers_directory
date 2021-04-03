import django_filters
from .models import *


class TeacherFilter(django_filters.FilterSet):
    subjects = django_filters.ModelMultipleChoiceFilter(
        field_name='subjects__name',
        to_field_name='name',
        queryset=Subject.objects.all()
    )

    class Meta:
        model = Teacher
        fields = {
            'last_name': ['startswith'],
        }

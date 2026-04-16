import django_filters as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id')
    name = filters.CharFilter(lookup_expr='icontains')  # поиск по части названия
    created_after = filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )

    class Meta:
        model = Course
        fields = ['author', 'name']

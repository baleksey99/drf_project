import django_filters as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    start_date = filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte'
    )
    end_date = filters.DateFilter(
        field_name='end_date',
        lookup_expr='lte'
    )

    class Meta:
        model = Course
        fields = ['start_date', 'end_date']

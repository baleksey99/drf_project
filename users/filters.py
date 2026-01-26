import django_filters as filters
from .models import Payment

class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course__id', lookup_expr='exact')
    lesson = filters.NumberFilter(field_name='lesson__id', lookup_expr='exact')
    method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date = filters.DateTimeFilter()


    ordering = filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
        ),
        field_labels={
            'payment_date': 'Дата оплаты (по возрастанию)',
            '-payment_date': 'Дата оплаты (по убыванию)',
        }
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'method', 'payment_date']

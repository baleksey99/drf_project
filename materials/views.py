# views.py
import stripe
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # ... остальные методы (как в вашем коде) ...

    @action(detail=True, methods=['post'], url_path='create-payment-session')
    def create_payment_session(self, request, pk=None):
        """
        Создаёт сессию Stripe Checkout для оплаты курса.
        """
        course = get_object_or_404(Course, pk=pk)

        try:
            # Создаём сессию Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': course.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            return Response({
                'session_id': checkout_session.id,
                'public_key': settings.STRIPE_PUBLISHABLE_KEY
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrModerator()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.author != self.request.user:
            raise PermissionDenied("Вы не можете создавать уроки для чужого курса")
        serializer.save(author=self.request.user)

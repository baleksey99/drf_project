from rest_framework import generics
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .filters import CourseFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrModerator
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CourseFilter

class CourseListView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrModerator]



class LessonListView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'description', 'preview']
    template_name = 'materials/course_update.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if (obj.author != request.user
                and not request.user.groups.filter(name='Модераторы').exists()):
            raise PermissionDenied("Нет прав на редактирование")
        return super().dispatch(request, *args, **kwargs)

class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if (obj.author != request.user
                and not request.user.groups.filter(name='Модераторы').exists()):
            raise PermissionDenied("Нет прав на удаление")
        return super().dispatch(request, *args, **kwargs)
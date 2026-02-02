from django.urls import path
from . import views

urlpatterns = [
    path('create-product/', views.CreateProductView.as_view(), name='create_product'),
    path('checkout/<str:price_id>/', views.CheckoutView.as_view(), name='checkout'),
]

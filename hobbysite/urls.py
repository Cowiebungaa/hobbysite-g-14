from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('detail_1/<int:pk>/', views.commission_detail_1, name='commission_detail_1'),
    path('detail_2/<int:pk>/', views.commission_detail_2, name='commission_detail_2'),
    path('detail_3/<int:pk>/', views.commission_detail_3, name='commission_detail_3'),
    path('detail_4/<int:pk>/', views.commission_detail_4, name='commission_detail_4'),
    path('detail_5/<int:pk>/', views.commission_detail_5, name='commission_detail_5'),
]

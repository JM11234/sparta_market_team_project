from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # 기본 URL에 대한 뷰 연결
]
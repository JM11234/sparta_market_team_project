from django.urls import path
from products import views


app_name = "products"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("product_detail/<int:pk>/", views.product_detail, name="product_detail"),
    path("delete/<int:pk>/", views.delete, name="product_delete"),
    path("update/<int:pk>", views.update, name="product_update"),
    path("review_create/<int:pk>", views.review_create, name="review_create"),
    path("review_delete/<int:pk>/", views.review_delete, name="review_delete"),
]

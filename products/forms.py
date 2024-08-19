from django import forms
from .models import Product, Review


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("seller", "is_available",)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        field = "__all__"
        exclude = ("user", "product",)

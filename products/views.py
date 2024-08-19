from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductsForm


def index(request):  ## 상품들 나열
    products = Product.objects.all()
    context = {"products":products}
    return render(request, "products/index.html", context)


@login_required
@require_http_methods(["GET","POST"])
def create(request):  # 모든 게시글 리스트
    if request.user.is_authenticated:
        if request.method == "POST":  ## 상품등록 버튼을 눌럿을때
            form = ProductsForm(data=request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                return redirect("index")
        else:
            form = ProductsForm()## 상품등록 브라우저를 보여줄때 (GET)
        context = {"form": form}
        return render(request, "products/create.html", context)
    return render(request, "accounts/login.html")

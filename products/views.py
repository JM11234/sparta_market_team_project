from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from .forms import ProductsForm, ReviewForm


def index(request):  # 메인홈페이지 (상품 리스트)
    products = Product.objects.all().order_by("-pk")
    context = {"products": products,
}
    return render(request, "products/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def create(request):  # 게시글 생성
    if request.user.is_authenticated:
        if request.method == "POST":  # 상품등록 버튼을 눌럿을때
            form = ProductsForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                return redirect("index")
        else:
            form = ProductsForm()  # 상품등록 브라우저를 보여줄때 (GET)
    context = {"form": form}
    return render(request, "products/create.html", context)


def product_detail(request, pk):  # 상품 상세 정보
    product = get_object_or_404(Product, id=pk)
    review_form = ReviewForm()
    product_reviews = product.reviews.all().order_by("-pk")
    context = {"product": product,
               "review_form": review_form,
               "product_reviews" : product_reviews,
               }
    return render(request, "products/product_detail.html", context)


@require_POST
def delete(request, pk):  # 상품 삭제
    if request.method == "POST":
        product = get_object_or_404(Product, id=pk)
        product.delete()
    return redirect("index")


@require_http_methods(["GET", "POST"])
def update(request, pk):  # 상품 수정
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":  # 수정완료 클릭 눌럿을시
        form = ProductsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:product_detail", product.pk)
    else:  # 수정 링크 진입시 GET 요청
        form = ProductsForm(instance=product)
    context = {"form": form,
               "product": product,
               }
    return render(request, "products/product_update.html", context)


@require_POST
def review_create(request, pk):  ## 해당상품 리뷰
    product = get_object_or_404(Product, id = pk)
    reviewer = request.user
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = reviewer
        review.product = product
        review.save()
        return redirect("products:product_detail", product.pk)
    

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    if request.user.is_authenticated:
        review.delete()
    return redirect('products:product_detail', review.product_id)
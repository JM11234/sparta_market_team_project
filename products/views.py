<<<<<<< HEAD
from itertools import product

from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Comment, Hashtag
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Count, Q

import logging
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Hashtag
from .forms import ProductForm
from django.shortcuts import render
from django.db.models import Q

from .forms import SearchForm

# 목록
def product_list(request):
    query = request.GET.get('query', '')  # 'query' 파라미터를 받아옴
    sort = request.GET.get('sort', '')  # 'sort' 파라미터를 받아옴

    # 초기 쿼리셋: 모든 제품
    products = Product.objects.all()


    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |  # 'user' 대신 'author' 사용
            Q(hashtags__content__icontains=query)
        ).distinct()

    # 정렬 옵션 처리
    if sort == 'likes':
        products = products.annotate(counts=Count('like_users')).order_by('-counts', '-pk')
    else:
        products = products.order_by('-pk')

    return render(request, 'product_list.html', {'products': products})


# 상품추기
@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            hashtags = form.cleaned_data['hashtags']
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                product.hashtags.add(hashtag)

            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm()
    context = {"form": form}
    return render(request, "create.html", context)


# 상세페이지
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm()
    comments = product.comments.all().order_by("-pk")
    context = {
        "product": product,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "product_detail.html", context)


# 삭제
@require_POST
def product_delete(request, pk):
    article = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        if article.author == request.user:
            article = get_object_or_404(Product, pk=pk)
            article.delete()
    return redirect("products:product_list")
=======
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
>>>>>>> 0fb0298094a4435c5cbaa056b4ab866d2cbc1e79


@login_required
@require_http_methods(["GET", "POST"])
<<<<<<< HEAD
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # 기존 해시태그 제거
            product.hashtags.clear()  # 해시태그 연결 제거

            hashtags = form.cleaned_data['hashtags']
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                product.hashtags.add(hashtag)

            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        

    context = {
        'form': form,
        'product': product,

    }
    return render(request, 'product_update.html', context)


# 댓글 추가
@require_POST
def comment_create(request, pk):
    article = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect("products:product_detail", article.pk)


# 댓글 삭제
@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:product_detail", pk)


@require_POST
def like_product(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)  # 찜 취소
        else:
            product.like_users.add(request.user)  # 찜 추가
        return redirect('products:product_detail', pk=pk)
    return redirect('accounts:login')


@login_required
def liked_products(request):
    products = request.user.liked_products.all()  # 사용자가 찜한 물건들
    return render(request, 'liked_products.html', {'products': products})
=======
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
>>>>>>> 0fb0298094a4435c5cbaa056b4ab866d2cbc1e79

from django.db import models
from django.conf import settings

class Hashtag(models.Model):
    content = models.CharField(max_length=50, unique=True)  # 해시태그는 고유해야 함

    def __str__(self):
        return self.content

class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True, default="images/default.png")  # 기본 이미지 설정
    view = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_products", blank=True
    )

    hashtags = models.ManyToManyField(Hashtag, blank=True)


    def __str__(self):
        return self.title

    @property
    def update_counter(self):
        self.view = self.view + 1
        self.save()


class Comment(models.Model):
    article = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updaetd_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Product(models.Model):
    name = models.CharField(max_length=200)  ## 상품이름
    description = models.TextField()  ## 상품 내용설명
    price = models.DecimalField(max_digits=10, decimal_places=0)  ## 상품가격, 최대 10자리 숫자와 소수점 2자리까지 허용
    is_available = models.BooleanField(default=True)   ## 판매 가능 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='main_images/', blank=True) ## 상품 메인이미지
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_product"
    )   ## 판매자와 판매자의 상품 외래키로 연결
    
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )   ## 해당상품의 리뷰들과 연결
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )  ## 리뷰를 작성한 유저와 연결
    
    comment = models.CharField(max_length=80)  ## 리뷰 내용
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.





@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or "index"
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("index")


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
        return redirect('index')


@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


@require_http_methods(["GET","POST"])
def cash_charge(request):  ## 캐쉬 충전
    if request.method == "POST":
        cash = request.POST.get('cash')
        if cash:
            try:
                cash_amount = int(cash)
                if cash_amount > 0:
                    request.user.cash += cash_amount
                    request.user.save()
                    messages.success(request, f'{cash_amount}원이 성공적으로 충전되었습니다.')
                    return redirect('index')
                else:
                    messages.error(request, '충전금액은 0보다 커야 합니다.')
            except ValueError:
                messages.error(request, '옳바른 금액을 입력해주세요.')
        else:
            messages.error(request, '충전할 금액을 입력해주세요.')
    return render(request, "accounts/cash_charge.html")
                
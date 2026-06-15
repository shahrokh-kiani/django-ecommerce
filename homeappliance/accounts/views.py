from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Customer
from django.contrib import messages
from shop.models import Order

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'این نام کاربری قبلاً ثبت شده'})

        if len(password) < 6:
            return render(request, 'register.html', {'error': 'رمز عبور باید حداقل ۶ کاراکتر باشد'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Customer.objects.create(user=user)
        login(request, user)
        return redirect('shop_main_page')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'ورود با موفقیت انجام شد.')
            return redirect('shop_main_page')
        else:
            return render(request, 'login.html', {'error': 'نام کاربری یا رمز اشتباه است'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('shop_main_page')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def profile_view(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-order_date')

    if request.method == 'POST':
        section = request.POST.get('section')


        if section == 'info':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            customer.phone = request.POST.get('phone', '')
            customer.save()
            messages.success(request, 'اطلاعات شخصی با موفقیت ذخیره شد')

        elif section == 'address':
            customer.address = request.POST.get('address', '')
            customer.province = request.POST.get('province', '')
            customer.city = request.POST.get('city', '')
            customer.postal_code = request.POST.get('postal_code', '')
            customer.save()
            messages.success(request, 'آدرس با موفقیت ذخیره شد')

        elif section == 'password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not request.user.check_password(old_password):
                messages.error(request, 'رمز عبور فعلی اشتباه است')
            elif new_password != confirm_password:
                messages.error(request, 'رمز عبور جدید و تکرار آن یکسان نیستند')
            elif len(new_password) < 6:
                messages.error(request, 'رمز عبور باید حداقل ۶ کاراکتر باشد')
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد')

        return redirect('profile')

    return render(request, 'profile.html', {
        'customer': customer,
        'orders': orders,
    })
    
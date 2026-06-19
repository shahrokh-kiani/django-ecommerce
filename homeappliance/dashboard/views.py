from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Order, Product, Category


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user, login_url='login')
def dashboard_home(request):
    context = {
        'order_count': Order.objects.count(),
        'pending_count': Order.objects.filter(status=False).count(),
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
    }
    return render(request, 'home.html', context)


@user_passes_test(is_staff_user, login_url='login')
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})


@user_passes_test(is_staff_user, login_url='login')
def order_toggle_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = not order.status
    order.save()
    messages.success(request, f'وضعیت سفارش #{order.id} به‌روزرسانی شد.')
    return redirect('dashboard:order_list')
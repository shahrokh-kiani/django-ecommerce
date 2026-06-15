from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Product, Rating, Category

def shop_main_page(request):
    all_products = Product.objects.annotate(avg_rating=Avg('ratings__score'))
    return render(request, 'index.html', {'products': all_products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = product.ratings.all().select_related('customer__user')
    avg_rating = ratings.aggregate(Avg('score'))['score__avg']

    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(product=product, customer=request.user.customer)
        except (Rating.DoesNotExist, Exception):
            pass

    return render(request, 'product_detail.html', {
        'product': product,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
    })

@login_required
def submit_rating(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        score = request.POST.get('score')
        Rating.objects.update_or_create(
            product=product,
            customer=request.user.customer,
            defaults={'score': score}
        )
    return redirect('product_detail', pk=pk)

def category_page(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).annotate(avg_rating=Avg('ratings__score'))
    categories = Category.objects.all()
    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })

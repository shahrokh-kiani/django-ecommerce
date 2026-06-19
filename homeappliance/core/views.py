from django.shortcuts import render
from django.db.models import Avg
from shop.models import Product


def landing(request):
    top_products = Product.objects.annotate(
        avg_rating=Avg('ratings__score')
    ).order_by('-id')[:8]
    return render(request, "landing.html", {"top_products": top_products})


def aboutus(request):
    return render(request, "about.html")
from .views import get_cart_data

def cart_context(request):
    try:
        items, total, count = get_cart_data(request)
    except Exception:
        items, total, count = [], 0, 0
    return {
        'cart_items': items,
        'cart_total': total,
        'cart_count': count,
    }
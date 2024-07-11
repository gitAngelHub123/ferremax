# app/context_processors.py
from .models import Post

def zero_stock_notification(request):
    zero_stock_products = Post.objects.filter(stock=0).exists()
    return {'zero_stock_products': zero_stock_products}

# context_processors.py
from .models import CartItem

# context_processors.py
from .models import CartItem

# context_processors.py
from .models import CartItem

# context_processors.py
from django.db import models
from .models import CartItem

def cart_count(request):
    cart_count = CartItem.objects.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    return {'cart_count': cart_count}

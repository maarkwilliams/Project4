from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    """ A view for all products, inc sorting and searching"""

    products = Products.objects.all()

    context = {
        'products': products,
    }
    
    return render(request, 'products/products.html', context)

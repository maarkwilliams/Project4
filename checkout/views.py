from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "No products in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51RpoqfBiMOwEfKNLusbGchh5MJh8Oo3lh4oAlkuUILPqWMbsmiwNrrdIS3NUDyk9wp3XNinKbMveVHZvbqfsDuEz00ChLihtaL',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
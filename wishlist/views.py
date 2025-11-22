from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Wishlist, WishlistItem

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.all()

    return render(request, "wishlist/wishlist.html", {
    "items": items
    })



@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)

    WishlistItem.objects.filter(wishlist=wishlist, product=product).delete()

    return redirect('wishlist')

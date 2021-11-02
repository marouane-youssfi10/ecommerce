from django.shortcuts import render, redirect
from store.models import Product
from .models import CartItem, Cart
from django.http import HttpResponse
# Create your views here.

# add _ in the first function to make it private
def _cart_id(request):
     cart = request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart

def add_cart(request, product_id):
     product = Product.objects.get(id=product_id)

     # this block for to take session_id
     try:
          cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the card_id present in session
     except Cart.DoesNotExist:
          cart = Cart.objects.create(cart_id=_cart_id(request))
     cart.save()

     # this block to create a new cartitems
     try:
          cart_item = CartItem.objects.get(product=product, cart=cart)
          cart_item.quantity += 1
          cart_item.save()
     except CartItem.DoesNotExist:
          cart_item = CartItem.objects.create(
               product=product,
               quantity=1,
               cart=cart,
          )
          cart_item.save()
     return HttpResponse(cart_item.quantity)
     exit()
     return redirect('cart')
def cart(request):
     return render(request, 'store/cart.html')
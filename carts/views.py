from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import CartItem, Cart
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

# add _ in the first function to make it private function
def _cart_id(request):
     cart = request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart

def add_cart(request, product_id):
     current_user = request.user
     # this if to take variations
     product = Product.objects.get(id=product_id)

     if current_user.is_authenticated:
          product_variation = []
          if request.method == 'POST':
               for item in request.POST:
                    key = item
                    value = request.POST[key]

                    print('key: ', key, ' ', 'value : ', value)
                    # if key != 'csrfmiddlewaretoken':
                    try:
                         variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                           variation_value__iexact=value)
                         product_variation.append(variation)
                    except:
                         pass
          # -----------------------------------------

          # this block to create a new cartitems
          is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
          if is_cart_item_exists:
               cart_item = CartItem.objects.filter(product=product, user=current_user)
               # existing_variations -> database
               # current_variations -> product_variation
               # item_id -> database
               ex_var_list = []
               id = []
               for item in cart_item:
                    existing_variations = item.variations.all()
                    ex_var_list.append(list(existing_variations))
                    id.append(item.id)

               # check ex_var_list is full with variation like color and size value
               if product_variation in ex_var_list:
                    # increase the cart item quantity
                    idex = ex_var_list.index(product_variation)
                    item_id = id[idex]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
               else:
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    # cart_item.quantity += 1
                    item.save()
          else:
               cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=current_user,
               )
               if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
               cart_item.save()
          # -----------------------------------------
          return redirect('cart')
     # ----------------------------------------------------------------------------------
     # -------------------------------------- else --------------------------------------
     # ----------------------------------------------------------------------------------
     # if the user is not authenticated
     else:
          product_variation = []
          if request.method == 'POST':
               for item in request.POST:
                    key = item
                    value = request.POST[key]

                    print('key: ', key, ' ', 'value : ', value)
                    # if key != 'csrfmiddlewaretoken':
                    try:
                         variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                         product_variation.append(variation)
                    except:
                         pass
          # -----------------------------------------

          # this block for to getting session_id
          try:
               cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the card_id present in session
          except Cart.DoesNotExist:
               cart = Cart.objects.create(cart_id=_cart_id(request))
          cart.save()
          # -----------------------------------------

          # this block to create a new cartitems
          is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
          if is_cart_item_exists:
               cart_item = CartItem.objects.filter(product=product, cart=cart)
               # existing_variations -> database
               # current_variations -> product_variation
               # item_id -> database
               ex_var_list = []
               id = []
               for item in cart_item:
                   existing_variations = item.variations.all()
                   ex_var_list.append(list(existing_variations))
                   id.append(item.id)

               print(ex_var_list)

               # check ex_var_list is full with variation like color and size value
               if product_variation in ex_var_list:
                    # increase the cart item quantity
                    idex = ex_var_list.index(product_variation)
                    item_id = id[idex]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
               else:
                    item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    # cart_item.quantity += 1
                    item.save()
          else:
               cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
               )
               if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
               cart_item.save()
          # -----------------------------------------
          return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     product = get_object_or_404(Product, id=product_id)
     try:
          cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
          if cart_item.quantity > 1:
              cart_item.quantity -= 1
              cart_item.save()
          else:
               cart_item.delete()
     except:
          pass
     return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     product = get_object_or_404(Product, id=product_id)
     cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
     cart_item.delete()
     return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
     tax = 0
     grand_total = 0
     try:
          """
               ila kan user authenticated stokih f cart_items sinon stoki sesseion key dyalo
               m3a product ou quantity ou variation 
          """
          if request.user.is_authenticated:
               cart_items = CartItem.objects.filter(user=request.user, is_active=True)
          else:
               cart = Cart.objects.get(cart_id=_cart_id(request))
               cart_items = CartItem.objects.filter(cart=cart, is_active=True)

          for cart_item in cart_items:
               total += (cart_item.product.price * cart_item.quantity)
               quantity += cart_item.quantity
          tax = (2 * total)/100
          grand_total = total + tax
     except ObjectDoesNotExist:
          print('------------ except --------------')


     context = {
          'total': total,
          'quantity': quantity,
          'cart_items': cart_items,
          'tax': tax,
          'grand_total': grand_total,
     }
     return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
     tax = 0
     grand_total = 0
     try:
          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_items = CartItem.objects.filter(cart=cart, is_active=True)
          for cart_item in cart_items:
               total += (cart_item.product.price * cart_item.quantity)
               quantity += cart_item.quantity
          tax = (2 * total) / 100
          grand_total = total + tax
     except ObjectDoesNotExist:
          print('------------ except --------------')

     context = {
          'total': total,
          'quantity': quantity,
          'cart_items': cart_items,
          'tax': tax,
          'grand_total': grand_total,
     }
     return render(request, 'store/checkout.html', context)
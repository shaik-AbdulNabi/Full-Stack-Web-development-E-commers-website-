from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum
from django.forms import formset_factory
from django.contrib import messages
from .forms import *
from .models import *
# Create your views here.
def p(request):
    d="tdapp"
    return render(request,"tdapp.html",{'d':d})

def uhome(request):
  
    user_id = request.session.get('user_id')
    uname = User.objects.get(id=user_id).user_name

    # Fetch all products
    products = Product.objects.filter(admin=1)#remove admin_id=1 to display all

    # Calculate discounted price for each product
    product_data = []
    for p in products:
        discounted_price  = discount(p.product_price,p.product_discount)
        product_data.append(
            {
            'id': p.id,
            'name': p.product_name,
            'price': p.product_price,
            'discount': p.product_discount,
            'discounted_price': round(discounted_price, 2),
            'quantity': p.product_quantity,
            'brand': p.product_brand,
            'category': p.product_category,
            'imageurl': p.product_url,
            }
        )
    wishlist_product_ids = []

    if user_id:
        wishlist_product_ids = Wishlist.objects.filter(user_id=user_id).values_list('product_id', flat=True)
        # Get top product purchased by the user
        top_product_data = (
            Sale.objects
            .filter(user_id=user_id)
            .values('product')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')[:3]
        )

        top_product = []  # Make it a list to hold 3 products

        for item in top_product_data:
            product = Product.objects.get(id=item['product'])
            discounted_price = discount(product.product_price, product.product_discount)

            top_product.append({
                'id': product.id,
                'name': product.product_name,
                'price': product.product_price,
                'discount': product.product_discount,
                'discounted_price': round(discounted_price, 2),
                'quantity': product.product_quantity,
                'brand': product.product_brand,
                'category': product.product_category,
                'imageurl': product.product_url,
            })



    return render(request, 'uhome.html', {
        'h': product_data,
        'uid': uname,
        'wishlist_product_ids': list(wishlist_product_ids),  # Needed for use in template
        'top_product': top_product
    })





def delete(request,id): 
    d=Product.objects.get(id=id)
    d.delete()
    return redirect('ahome')

def cproductdelete(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')


def cartadd(request,id): 
    uid=request.session.get('user_id')
    user = User.objects.get(id=uid)
    product = Product.objects.get(id=id)
    admin = product.admin # If Product has no FK to Admin, and you set it manually in Cart

    # Create the cart item
    existing_item = Cart.objects.filter(user=user, product=product, admin=admin).first()
    
    if not existing_item:
        Cart.objects.create(user=user, product=product, admin=admin)
    return redirect('uhome')




def discount(op, dp):
    return op - (op * dp / 100)


def cart(request): 
    uid = request.session.get('user_id')
    user = User.objects.get(id=uid)

    # Get all cart items for the user (no admin filter)
    cart_items = Cart.objects.filter(user_id=uid).select_related('product', 'admin')

    cart_data = []
    form_data = []
    total_discount_price = 0

    for item in cart_items:
        product = item.product
        dp = discount(product.product_price, product.product_discount)
        total_discount_price += dp

        cart_data.append({
            "cart_id": item.id,
            "product_id": product.id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_quantity": product.product_quantity,
            "product_brand": product.product_brand,
            "product_category": product.product_category,
            "product_discount": product.product_discount,
            "product_image": product.product_url,
            "discount_price": round(dp, 2),
            "admin_name": item.admin.admin_name,
            "admin_shopname": item.admin.admin_shopname
        })

        form_data.append({
            "product_id": product.id,
            "quantity": 1  # default value
        })

    BuyFormSet = formset_factory(BuyItemForm, extra=0)
    formset = BuyFormSet(initial=form_data)

    # Combine formset and cart data to use in template
    combined = zip(formset.forms, cart_data)

    return render(request, 'cart.html', {
        'uname': user.user_name,
        'formset': formset,
        'combined_data': combined,  # use this in template loop
        'total_discount_price': round(total_discount_price, 2)
    })



def wishlistadd(request, id): 
    uid = request.session.get('user_id')
    user = User.objects.get(id=uid)
    product = Product.objects.get(id=id)
    aid=product.admin
    # Check only by user and product
    existing_item = Wishlist.objects.filter(user=user, product=product).first()
    
    if existing_item:
        existing_item.delete()
    else:
        Wishlist.objects.create(user=user, product=product, admin=aid)

    return redirect('uhome')


def wproductdelete(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    wishlist_item.delete()
    return redirect('wishlist')

def wishlist(request): 
    uid = request.session.get('user_id')
    user = User.objects.get(id=uid)
    wishlist_items = Wishlist.objects.filter(user_id=uid, admin_id=1).select_related('product', 'admin')#if you needs to display all shops data remove admin_id=1

    wishlist_data = []
    total_discount_price = 0

    for item in wishlist_items:
        dp = discount(item.product.product_price, item.product.product_discount)
        total_discount_price += dp

        wishlist_data.append({
            "wishlist_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.product_name,
            "product_price": item.product.product_price,
            "product_quantity": item.product.product_quantity,
            "product_brand": item.product.product_brand,
            "product_category": item.product.product_category,
            "product_discount": item.product.product_discount,
            "discount_price": dp,
            "admin_name": item.admin.admin_name,
            "admin_shopname": item.admin.admin_shopname,
            "product_image":item.product.product_url,
        })

    username = user.user_name
    return render(request, 'wishlist.html', {
        'wishlist_data': wishlist_data,
        'uname': username,
        'total_discount_price': round(total_discount_price, 2)  # optional rounding
    })


def buy_items(request):
    BuyFormSet = formset_factory(BuyItemForm)

    if request.method == "POST":
        formset = BuyFormSet(request.POST)

        if formset.is_valid():
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)

            for form in formset:
                product_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    continue

                if product.product_quantity >= quantity:
                    price = product.product_price - (product.product_price * product.product_discount / 100)

                    Sale.objects.create(
                        user=user,
                        admin=product.admin,
                        product=product,
                        quantity=quantity,
                        price=price
                    )

                    product.product_quantity -= quantity
                    product.save()

            return redirect('uhome')

    return redirect('cart')

































# def cart(request): 
#     uid=request.session.get('user_id')
#     user=User.objects.get(id=uid)
#     cart_items = Cart.objects.filter(user_id=uid).select_related('product', 'admin')

#     cart_data = [
#         {
#             # "user_name": item.user.user_name,
#             "product_name": item.product.product_name,
#             "product_price": item.product.product_price,
#             "product_quantity": item.product.product_quantity,
#             "product_brand": item.product.product_brand,
#             "product_category": item.product.product_category,
#             "product_discount": item.product.product_discount,
#             "discount_price":discount(item.product.product_price,item.product.product_discount),
#             "admin_name": item.admin.admin_name,
#             "admin_shopname": item.admin.admin_shopname
#         }
#         for item in cart_items
#     ]
#     username=user.user_name

#     return render(request, 'cart.html', {'cart_data': cart_data,"uname":username})
# def discount(op,dp):
#     r=op-(op*dp/100)
#     return r
# # discount(item.product.product_price,item.product.product_discount)
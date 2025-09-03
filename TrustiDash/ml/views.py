from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from tdapp.models import *
from .forms import *
# Create your views here.
def h(request):
    p="ml"
    return render(request,"ml.html",{'p':p})


def ahome(request,id=None):
    admin_id = request.session.get('admin_id')
    admin = Admin.objects.get(id=admin_id)  # Get the logged-in admin
    instance = get_object_or_404(Product, id=id) if id else None


    if request.method == 'POST':
        form = ProductForm(request.POST,instance=instance)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save to DB yet
            product.admin = admin             # Assign the admin manually
            product.save()                    # Now save the object
            return redirect('ahome')          # Redirect after saving
    else:
        form = ProductForm(instance=instance)

    h = Product.objects.filter(admin=admin)  # Only show products by that admin
    return render(request, 'ahome.html', {'form': form, 'h': h})

def upload(request,id=None):
    admin_id = request.session.get('admin_id')
    admin = Admin.objects.get(id=admin_id)  # Get the logged-in admin
    instance = get_object_or_404(Product, id=id) if id else None


    if request.method == 'POST':
        form = ProductForm(request.POST,instance=instance)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save to DB yet
            product.admin = admin             # Assign the admin manually
            product.save()                    # Now save the object
            return redirect('upload')          # Redirect after saving
    else:
        form = ProductForm(instance=instance)

    h = Product.objects.filter(admin=admin)  # Only show products by that admin
    return render(request, 'newupload.html', {'form': form, 'h': h})


def dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')

    # Get all sales by this admin
    sales = Sale.objects.filter(admin_id=admin_id)

    # Annotate each sale with revenue
    sales = sales.annotate(
        revenue=ExpressionWrapper(F('quantity') * F('price'), output_field=FloatField())
    )

    # Calculate totals
    total_quantity = 0
    total_revenue = 0.0
    user_ids = set()

    for sale in sales:
        total_quantity += sale.quantity
        total_revenue += sale.revenue
        user_ids.add(sale.user_id)

    # Top 5 products by quantity sold
    top_products = (
        Sale.objects.filter(admin_id=admin_id)
        .values('product__product_name')
        .annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum(ExpressionWrapper(F('quantity') * F('price'), output_field=FloatField()))
        )
        .order_by('-total_sold')[:5]
    )

    # Bottom 5 products by quantity sold
    bottom_products = (
        Sale.objects.filter(admin_id=admin_id)
        .values('product__product_name')
        .annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum(ExpressionWrapper(F('quantity') * F('price'), output_field=FloatField()))
        )
        .order_by('total_sold')[:5]
    )

    context = {
        'total_quantity': total_quantity,
        'total_revenue': total_revenue,
        'total_users': len(user_ids),
        'top_products': top_products,
        'bottom_products': bottom_products,
    }

    return render(request, 'dashbord.html', context)

def customers(request):
    context="customers"
    return render(request, 'customers.html')

def analatics(request):
    context="analatics"
    return render(request, 'analytics.html')
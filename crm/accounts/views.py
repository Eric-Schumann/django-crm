from django.shortcuts import render, redirect
from accounts.models import Product, Order, Customer
from .forms import OrderForm

def home(request):
    orders = Order.objects.all().order_by('-status')
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = { 
        'orders': orders, 
        'customers': customers, 
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', { 'products': products })

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    return render(request, 'accounts/customer.html', { 'customer' : customer, 'orders': orders })
    
def create_order(request):
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'accounts/order_form.html', { 'form': form })
    
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = { 'form': form }
    
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accounts/order_form.html', context)
    
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    context = { 'item': order }
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    return render(request, 'accounts/delete.html', context)
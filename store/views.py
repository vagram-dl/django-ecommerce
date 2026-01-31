from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__gte=max_price)
    return render(request,'store/product_list.html', {'products': products})

def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request, 'store/product_detail.html', {'product':product})

def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)

    cart = request.session.get('cart',{})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart',{})
    products = []
    total = 0

    for product_id,quantity in cart.items():
        product = Product.objects.get(id=product_id)
        products.append({
            'product': product,
            'quantity':quantity,
            'subtotal':product.price * quantity,
        })

        total += product.price * quantity

    return render(request, 'store/cart.html',{
        'products':products,
        'total':total,
    })

# Create your views here.

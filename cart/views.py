from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from app.models import Course
from django.contrib import messages 
from app.forms import CourseForm
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, QuantityUpdateForm
# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Course, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_add_net_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Course, id=product_id)
    # Bu yerda foydalanuvchidan savatchaga qo'shish miqdorini olish uchun POST so'rovini ishlatmasdan formani yaratamiz
    form = CartAddProductForm()

    # Foydalanuvchi tanlagan mahsulotni savatchaga qo'shish
    cart.add(course=product, quantity=1, override_quantity=True)
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Course, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        # Handle product creation form
        create = CourseForm(request.POST, request.FILES)
        if create.is_valid():
            post = create.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post successfully created.')
            return redirect('/')
        else:
            messages.error(request, 'Failed to create post.')

        # Handle order creation form
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            # Clear the cart
            cart.clear()
            messages.success(request, 'Order created successfully!')
            return render(request, 'orders/create.html', {'order': order})
        else:
            messages.error(request, 'Failed to create order.')

        # Handle update quantity form
        update_quantity_form = QuantityUpdateForm(request.POST)
        if update_quantity_form.is_valid():
            product_id = update_quantity_form.cleaned_data['product_id']
            quantity = update_quantity_form.cleaned_data['quantity']
            cart.add(product_id=product_id, quantity=quantity, override_quantity=True)
            messages.success(request, 'Quantity updated successfully.')
        else:
            messages.error(request, 'Failed to update quantity.')

    else:
        create = CourseForm()
        form = OrderCreateForm()
        update_quantity_form = QuantityUpdateForm()

    orders = Order.objects.all()

    # Add update quantity form to each item in the cart
    for item in cart:
        item['update_quantity_form'] = QuantityUpdateForm(initial={
            'product_id': item['course'].id,
            'quantity': item['quantity'],
        })

    return render(request, 'cart/cart.html', {'cart': cart, 'create': create, 'orders': orders, 'form': form, 'update_quantity_form': update_quantity_form})

def update_quantity(request, product_id):
    cart = Cart(request)
    try:
        product = Course.objects.get(id=product_id)
    except Course.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('/')  # Replace 'your_redirect_url' with the appropriate URL

    if request.method == 'POST':
        form = QuantityUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product=product, quantity=quantity, override_quantity=True)
            # You may redirect to a different page or render a success message here
            return redirect('cart:update_quantity', product.id)  # Replace 'your_redirect_url' with the appropriate URL
    else:
        form = QuantityUpdateForm(initial={'quantity': cart.cart[str(product.id)]['quantity']})

    return render(request, 'shop/update_quantity.html', {'form': form, 'product': product})

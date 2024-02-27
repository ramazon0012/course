from django.shortcuts import render, redirect
from .models import OrderItem
from django.contrib import messages
from cart.forms import CartAddProductForm
from app.forms import CourseForm
from .models import Order
# Create your views here.
from .forms import OrderCreateForm, OrderForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                delivery=form.cleaned_data['delivery'],
                status=form.cleaned_data['status'],
                paid=form.cleaned_data['paid']
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            # Clear the cart
            cart.clear()

            return render(request, 'orders/order/create.html', {'order': order})

    else:
        form = OrderForm()
        
    if request.method == 'POST':
        create = CourseForm(request.POST, request.FILES)
        if create.is_valid():   
            post = create.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post successfully created.')
            return redirect('/')
        else:
            pass
    else:
        create = CourseForm()

    orders = Order.objects.all()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form, 'create': create, 'orders': orders})

def delete_order(request, order_id, user_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('account', user_id)  # O'zgartiring "your_redirect_url" ni tegishli yo'lga
    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('account', user_id)
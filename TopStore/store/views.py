import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from TopStore.products.models import Product
from TopStore.store.forms import ContactForm, OrderForm
from TopStore.store.models import Order, OrderItem


# Create your views here.


def store(request):
    products = Product.objects.order_by('id')
    for product in products:
        product.likes_count = product.like_set.count()
    trending_products = sorted(products, key=lambda x: -x.likes_count)[:4]
    new_additions = Product.objects.order_by('-id')[:4]

    context = {
        'trending_products': trending_products,
        'new_additions': new_additions,
    }

    return render(request, 'store/store.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def cart(request):
    order, is_completed = Order.objects.get_or_create(user=request.user, is_completed=False)

    items = order.orderitem_set.all()
    for item in items:
        if not item.product_id:
            item.delete()

    items = order.orderitem_set.all().order_by('product_id')
    cart_items = order.total_cart_items_count
    request.session['cart_items_count'] = cart_items

    context = {
        'items': items,
        'order': order,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def checkout(request):
    user = request.user
    order, is_completed = Order.objects.get_or_create(user=user, is_completed=False)

    items = order.orderitem_set.all()
    for item in items:
        if not item.product_id:
            item.delete()

    items = order.orderitem_set.all().order_by('product_id')
    cart_items = order.total_cart_items_count
    request.session['cart_items_count'] = cart_items

    if request.method == 'POST':
        form = OrderForm(request.POST, initial={'order': order.id, 'user': user.id})
        if form.is_valid():
            form.save()
            order.is_completed = True
            order.date_ordered = datetime.now()
            order.save()
            request.session['cart_items_count'] = 0
            Order.objects.create(user=user, is_completed=False)
            return render(request, 'store/checkout_successful.html')
    else:
        form = OrderForm(initial={'order': order.id, 'user': user.id})

    context = {
        'items': items,
        'order': order,
        'form': form,
    }

    return render(request, 'store/checkout.html', context)


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            form = ContactForm(request.POST, initial={'name': user.username, 'email': user.email})
        else:
            form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'store/contact_message.html')
    else:
        if user.is_authenticated:
            form = ContactForm(initial={'name': user.username, 'email': user.email})
        else:
            form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'store/contact.html', context)


def update_item(request):
    if not request.body:
        return redirect('store')

    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
        request.session['cart_items_count'] += 1
    elif action == 'remove':
        order_item.quantity -= 1
        request.session['cart_items_count'] -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added/removed', safe=False)

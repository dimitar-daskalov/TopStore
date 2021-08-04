from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from TopStore.accounts.forms import SingInForm, SingUpForm, ProfileDetailsForm
from TopStore.accounts.models import Profile
from TopStore.products.models import Like
from TopStore.store.models import Order, OrderInformation


# Create your views here.


def sing_in_user(request):
    if request.method == 'POST':
        form = SingInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            order = Order.objects.get(user=user, is_completed=False)
            request.session['cart_items_count'] = order.total_cart_items_count

            return redirect('store')
    else:
        form = SingInForm()

    context = {
        'form': form,
    }

    return render(request, 'account/sign_in_user.html', context)


def sing_out_user(request):
    logout(request)
    return redirect('store')


def sing_up_user(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store')
    else:
        form = SingUpForm()

    context = {
        'form': form,
    }

    return render(request, 'account/sing_up_user.html', context)


@login_required(login_url=reverse_lazy('sing in user'))
def details_profile_user(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileDetailsForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        if form.is_valid():
            form.save()
            return redirect('details account user')
    else:
        form = ProfileDetailsForm(instance=profile)

    liked_products = Like.objects.filter(user_id=request.user.id)

    context = {
        'form': form,
        'liked_products': liked_products,
        'account': profile,
    }

    return render(request, 'account/profile_user.html', context)


@login_required(login_url=reverse_lazy('sing in user'))
def completed_orders_user(request):
    user = request.user
    if user.is_staff:
        return redirect('all products')

    orders = Order.objects.filter(user=user, is_completed=True)

    for order in orders:
        order.address = OrderInformation.objects.filter(order=order.id).values_list('address', flat=True)[0]
        order.city = OrderInformation.objects.filter(order=order.id).values_list('city', flat=True)[0]
        order.telephone_number = \
            OrderInformation.objects.filter(order=order.id).values_list('telephone_number', flat=True)[0]
        order.zip_code = OrderInformation.objects.filter(order=order.id).values_list('zip_code', flat=True)[0]
        order.items = ', '.join(order.orderitem_set.all().values_list('product__name', flat=True))

    paginator = Paginator(orders, 5)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
    }

    return render(request, 'account/orders_information_user.html', context)

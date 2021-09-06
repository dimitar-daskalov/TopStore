from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from TopStore.accounts.forms import SignInForm, SignUpForm, ProfileDetailsForm
from TopStore.accounts.models import Profile
from TopStore.products.models import Like
from TopStore.store.forms import ContactForm
from TopStore.store.models import Order, OrderInformation, ContactMessage


# Create your views here.


def sign_in_user(request):
    if request.user.is_authenticated:
        return redirect('all products')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            order = Order.objects.get(user=user, is_completed=False)
            request.session['cart_items_count'] = order.total_cart_items_count
            return redirect('store')

    else:
        form = SignInForm()

    context = {
        'form': form,
    }

    return render(request, 'account/sign_in_user.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def sign_out_user(request):
    logout(request)
    return redirect('store')


def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect('all products')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            order, created = Order.objects.get_or_create(user=user, is_completed=False)
            request.session['cart_items_count'] = order.total_cart_items_count
            return redirect('store')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'account/sign_up_user.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
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

    liked_products = Like.objects.filter(user_id=request.user.id).order_by('-product_id')

    paginator = Paginator(liked_products, 4)
    page = request.GET.get('page')

    try:
        liked_products = paginator.page(page)
    except PageNotAnInteger:
        liked_products = paginator.page(1)
    except EmptyPage:
        liked_products = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'liked_products': liked_products,
        'account': profile,
    }

    return render(request, 'account/profile_user.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def completed_orders_user(request):
    user = request.user
    if user.is_staff:
        orders = Order.objects.filter(is_completed=True).order_by('-date_ordered')
    else:
        orders = Order.objects.filter(user=user, is_completed=True).order_by('-date_ordered')

    for order in orders:
        order.address = OrderInformation.objects.filter(order=order.id).values_list('address', flat=True)[0]
        order.city = OrderInformation.objects.filter(order=order.id).values_list('city', flat=True)[0]
        order.telephone_number = \
            OrderInformation.objects.filter(order=order.id).values_list('telephone_number', flat=True)[0]
        order.zip_code = OrderInformation.objects.filter(order=order.id).values_list('zip_code', flat=True)[0]
        order.items = '| '.join(order.orderitem_set.all().values_list('product__name', flat=True))

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


@login_required(login_url=reverse_lazy('sign in user'))
def contact_messages_users(request):
    if not request.user.is_staff:
        return redirect('all products')

    contact_messages = ContactMessage.objects.all().order_by('-id')

    paginator = Paginator(contact_messages, 5)
    page = request.GET.get('page')

    try:
        contact_messages = paginator.page(page)
    except PageNotAnInteger:
        contact_messages = paginator.page(1)
    except EmptyPage:
        contact_messages = paginator.page(paginator.num_pages)

    context = {
        'contact_messages': contact_messages,
    }

    return render(request, 'account/contact_messages_staff_user.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def contact_message_reply(request, pk):
    if not request.user.is_staff:
        return redirect('all products')

    contact_message = ContactMessage.objects.get(pk=pk)

    contact_message_form = ContactForm(initial=contact_message.__dict__)

    for field in contact_message_form.fields:
        contact_message_form.fields[field].disabled = True

    if request.method == 'POST':
        reply_form = ContactForm(request.POST,
                                 initial={'name': contact_message.name, 'email': contact_message.email})

        if reply_form.is_valid():
            form = reply_form.save(commit=False)
            name = form.name
            mail_subject = f'{name.capitalize()} response email from TopStore.'
            to_email = form.email
            message = form.message
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            contact_message.answered = True
            contact_message.save()

            return redirect('contact messages users')
    else:
        reply_form = ContactForm(initial={'name': contact_message.name, 'email': contact_message.email})

    context = {
        'contact_message_form': contact_message_form,
        'contact_message_reply_form': reply_form,
    }

    return render(request, 'account/contact_message_reply.html', context)

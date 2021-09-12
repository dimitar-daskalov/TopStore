from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from TopStore.accounts.forms import SignInForm, SignUpForm, ProfileDetailsForm, \
    BootstrapResetPasswordForm, BootstrapSetPasswordForm, BootstrapChangePasswordForm
from TopStore.accounts.models import Profile
from TopStore.products.models import Like
from TopStore.store.forms import ContactForm
from TopStore.store.models import Order, OrderInformation, ContactMessage

# Create your views here.

UserModel = get_user_model()


def sign_in_user(request):
    if request.user.is_authenticated:
        return redirect('all products')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            order, created = Order.objects.get_or_create(user=user, is_completed=False)
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/activate_email_user.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'account/activation_needed_user.html')

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


def activate_user_email(request, uidb64, token):
    """
    Decodes the user id from activation link and checks the token.
    Sets the user as active and renders the sign_in_user view on success.
    Otherwise error msg is rendered.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('sign in user')
    else:
        return render(request, 'account/activation_invalid_user.html')


def custom_password_reset_view(request):
    if request.method == 'POST':
        form = BootstrapResetPasswordForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['email']
            user_email = UserModel.objects.filter(email=to_email)
            current_site = get_current_site(request)
            if user_email.exists():
                for user in user_email:
                    mail_subject = 'Password reset TopStore'
                    message = render_to_string(
                        'account/password_reset_message_user.html',
                        {
                            'username': user.username,
                            'email': user.email,
                            'domain': current_site.domain,
                            'site_name': 'TopStore',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        })
                    try:
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                    except:
                        return HttpResponseNotFound()

                    return redirect('password_reset_done')
    else:
        form = BootstrapResetPasswordForm()

    context = {
        'form': form,
    }

    return render(request, 'account/reset_password_user.html', context)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/change_password_user.html'
    form_class = BootstrapChangePasswordForm


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/change_password_done_user.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/reset_password_done_user.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/reset_password_confirm_user.html'
    form_class = BootstrapSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/reset_password_complete_user.html'

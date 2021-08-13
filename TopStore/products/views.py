from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from TopStore.products.forms import ProductForm, ReviewForm
from TopStore.products.models import Product, Like
from TopStore.shared.filter_types import types_filter


# Create your views here.


@login_required(login_url=reverse_lazy('sign in user'))
def create_product(request):
    if not request.user.is_staff:
        return redirect('store')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'product/create_product.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def update_product(request, pk):
    if not request.user.is_staff:
        return redirect('store')

    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'product/update_product.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def delete_product(request, pk):
    if not request.user.is_staff:
        return redirect('store')

    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        product.delete()
        return redirect('store')

    context = {
        'product': product,
    }
    return render(request, 'product/delete_product.html', context)


@login_required(login_url=reverse_lazy('sign in user'))
def like_product(request, pk):
    if request.user.is_staff:
        return redirect('store')

    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    like_object_by_user = product.like_set.filter(user_id=request.user.id) \
        .first()
    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = Like(
            product=product,
            user=request.user,
        )
        like.save()
    return redirect('details product', product.id)


@login_required(login_url=reverse_lazy('sign in user'))
def review_product(request, pk):
    if request.user.is_staff:
        return redirect('store')

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()

    return redirect('details product', pk)


def details_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    product.likes_count = product.like_set.count()

    is_liked_by_user = product.like_set.filter(user_id=request.user.id) \
        .exists()

    context = {
        'product': product,
        'review_form': ReviewForm(
            initial={'product_pk': pk}
        ),
        'reviews': product.review_set.all(),
        'is_liked': is_liked_by_user,
    }

    return render(request, 'product/details_product.html', context)


def all_products(request):
    all_product_list = Product.objects.all().order_by('id')

    # returns the unique types for the dropdown menu
    types = types_filter(all_product_list)

    paginator = Paginator(all_product_list, 8)
    page = request.GET.get('page')

    try:
        all_product_list = paginator.page(page)
    except PageNotAnInteger:
        all_product_list = paginator.page(1)
    except EmptyPage:
        all_product_list = paginator.page(paginator.num_pages)

    context = {
        'all_products': all_product_list,
        'types': types,
    }

    return render(request, 'product/all_products.html', context)


def filter_products(request, product_type):
    product_type = product_type[:-1] if product_type != 'Headphones' else product_type
    filtered_products = Product.objects.filter(type=product_type)
    products = Product.objects.all()

    # returns the unique types for the dropdown menu
    types = types_filter(products)

    paginator = Paginator(filtered_products, 8)
    page = request.GET.get('page')

    try:
        filtered_products = paginator.page(page)
    except PageNotAnInteger:
        filtered_products = paginator.page(1)
    except EmptyPage:
        filtered_products = paginator.page(paginator.num_pages)

    context = {
        'all_products': filtered_products,
        'types': types
    }

    return render(request, 'product/all_products.html', context)

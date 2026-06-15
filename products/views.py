from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from .models import Product
from accounts.models import UserCustomer, Contact
from checkout.models import Order
from .forms import CommentForm, ProductForm
from accounts.forms import GiftACanForm


def all_products(request):
    """View to display all products."""

    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """View to display a single product."""

    product = get_object_or_404(Product, pk=product_id)
    comment_form = CommentForm()
    comments = product.comments.all()  # type: ignore
    gift_form = GiftACanForm()
    contacts = []

    if request.user.is_authenticated:
        user_customer = UserCustomer.objects.filter(user=request.user).first()
        if user_customer:
            contacts = user_customer.customer.contact_set.all()  # type: ignore

    context = {
        "product": product,
        "comment_form": comment_form,
        "comments": comments,
        "gift_form": gift_form,
        "contacts": contacts,
    }
    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # ← stocke le produit
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please check the form.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_detail', args=[product.id]))  # type: ignore
        else:
            messages.error(request, 'Failed to update product.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect(reverse('all_products'))


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            user_customer = UserCustomer.objects.filter(user=request.user).first()
            customer = user_customer.customer if user_customer else None

            # display_name overrides name/surname if set
            if customer and customer.display_name:
                comment.name = customer.display_name  # type: ignore
                comment.surname = ''  # type: ignore
            else:
                comment.name = (customer.name if customer and customer.name else request.user.username)  # type: ignore
                comment.surname = (customer.surname if customer and customer.surname else '')  # type: ignore

            comment.product = product
            if customer:
                order = Order.objects.filter(customer=customer, items__product=product).last()
                comment.order = order
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))  # type: ignore
        else:
            messages.error(request, 'Failed to add comment. Please check the form.')
    else:
        form = CommentForm()

    return render(request, 'products/add_comment.html', {'form': form, 'product': product})


@login_required
def gift_a_can_view(request, product_id):
    """View for gifting a can to a friend."""
    product = get_object_or_404(Product, pk=product_id)

    user_customer = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customer.customer if user_customer else None

    if not customer:
        messages.warning(request, 'Please complete your profile before gifting a can.')
        return redirect(reverse('profile'))

    contacts = customer.contact_set.all()  # type: ignore

    if request.method == "POST":
        existing_contact_id = request.POST.get("existing_contact")
        form = GiftACanForm(request.POST)

        if existing_contact_id:
            contact = get_object_or_404(
                Contact,
                pk=existing_contact_id,
                customer=customer,
            )
        elif form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.ip_address = request.META.get('REMOTE_ADDR', '')
            contact.save()
        else:
            messages.error(request, 'Failed to gift a can. Please check the form.')
            return render(request, 'products/gift_a_can.html', {
                'form': form,
                'product': product,
                'contacts': contacts,
            })

        customer.promo_discount = Decimal('10')
        customer.save()

        subject = render_to_string(
            'products/gift_email_subject.txt',
            {'product': product, 'customer': customer}
        )
        body = render_to_string(
            'products/gift_email_body.txt',
            {'product': product, 'customer': customer, 'contact': contact}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [contact.email]
        )
        messages.success(request, 'You gifted a can! You get 10% off your next order!')
        return redirect(reverse('product_detail', args=[product.id]))  # type: ignore
    else:
        form = GiftACanForm()

    return render(request, 'products/gift_a_can.html', {
        'form': form,
        'product': product,
        'contacts': contacts,
    })

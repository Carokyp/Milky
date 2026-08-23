from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html

from .models import Product
from accounts.models import UserCustomer, Contact
from checkout.models import Order
from .email_utils import build_gift_email_context
from .forms import ReviewForm, ProductForm
from accounts.forms import GiftACanForm


def superuser_required(view_func):
    """Redirect non-superusers to home with an error message."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(
                request, 'Sorry, only store owners can do that.'
            )
            return redirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return wrapper


def all_products(request):
    """Display all products."""
    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)


REVIEWS_PER_PAGE = 3


def product_detail(request, product_id):
    """Display a single product with its paginated reviews."""
    product = get_object_or_404(Product, pk=product_id)
    review_form = ReviewForm()
    reviews_list = product.reviews.order_by("-id")  # type: ignore
    paginator = Paginator(reviews_list, REVIEWS_PER_PAGE)
    reviews = paginator.get_page(request.GET.get("page"))

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "products/reviews_list.html", {"reviews": reviews}, request=request
        )
        return JsonResponse({"html": html})

    context = {
        "product": product,
        "review_form": review_form,
        "reviews": reviews,
    }
    return render(request, "products/product_detail.html", context)


def gift_page_view(request):
    """Handle the standalone gift-a-can page and its submission."""
    products = Product.objects.filter(is_available=True)
    contacts = []
    customer = None
    gift_in_progress = request.session.get('gift')

    if request.user.is_authenticated:
        user_customer = UserCustomer.objects.filter(
            user=request.user
        ).first()
        customer = user_customer.customer if user_customer else None
        if customer:
            contacts = customer.contact_set.all()  # type: ignore

    def render_gift_page(form):
        return render(request, 'products/gift_page.html', {
            'products': products,
            'contacts': contacts,
            'form': form,
            'customer': customer,
            'gift_in_progress': gift_in_progress,
        })

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))

        if not customer:
            messages.warning(
                request,
                'Please complete your profile before gifting a can.',
            )
            return redirect(reverse('profile'))

        if gift_in_progress:
            messages.error(request, 'You can only gift one can per order.')
            return redirect(reverse('gift_page'))

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        if not product.is_available:
            messages.error(request, 'This product is not available.')
            return redirect(reverse('gift_page'))

        personal_message = request.POST.get('personal_message', '').strip()
        existing_contact_id = request.POST.get('existing_contact')
        form = GiftACanForm(request.POST)

        if existing_contact_id:
            contact = get_object_or_404(
                Contact, pk=existing_contact_id, customer=customer
            )
        elif form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.ip_address = request.META.get('REMOTE_ADDR', '')
            contact.save()
        else:
            messages.error(
                request, 'Failed to gift a can. Please check the form.'
            )
            return render_gift_page(form)

        request.session['gift'] = {
            'product_id': str(product.id),  # type: ignore
            'contact_id': contact.id,  # type: ignore
            'personal_message': personal_message,
        }

        messages.success(
            request,
            format_html(
                '<strong>{}</strong> added to your cart for '
                '<strong>{}</strong>! You get <strong>10% off</strong> '
                'this order at checkout.',
                product.name, contact.name,
            ),
            extra_tags="gift",
        )
        return redirect(reverse('view_cart'))

    form = GiftACanForm()
    return render_gift_page(form)


# TODO: Remove before deployment
@login_required
@superuser_required
def preview_gift_email(request):
    """Render the real gift-a-can email in the browser, for styling work.

    Store-owner only. Shows real contact/customer data from the most
    recent gift.
    """
    contact = Contact.objects.order_by('-id').first()
    product = Product.objects.filter(is_available=True).first()
    if not contact or not product:
        return HttpResponse(
            "No gift in the database yet — gift a can first."
        )

    context = build_gift_email_context(
        request, product, contact.customer, contact,
        "Enjoy this can, you deserve it!"
    )
    html_body = render_to_string('products/gift_email_body.html', context)
    return HttpResponse(html_body)


@login_required
@superuser_required
def add_product(request):
    """Create a new product (store owners only)."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, 'Product added successfully!', extra_tags="product"
            )
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product. Please check the form.'
            )
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
@superuser_required
def edit_product(request, product_id):
    """Edit an existing product (store owners only)."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Product updated successfully!',
                extra_tags="product",
            )
            return redirect(reverse(
                'product_detail', args=[product.id]  # type: ignore
            ))
        else:
            messages.error(request, 'Failed to update product.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(
        request,
        'products/edit_product.html',
        {'form': form, 'product': product},
    )


@login_required
@superuser_required
def delete_product(request, product_id):
    """Delete a product (store owners only)."""
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(
        request, 'Product deleted successfully!', extra_tags="product"
    )
    return redirect(reverse('all_products'))


@login_required
def add_review(request, product_id):
    """Add a review to a product, submitted by the logged-in user."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)

            user_customer = UserCustomer.objects.filter(
                user=request.user
            ).first()
            customer = user_customer.customer if user_customer else None

            review.name = (  # type: ignore
                customer.name if customer and customer.name
                else request.user.username
            )
            review.surname = (  # type: ignore
                customer.surname if customer and customer.surname
                else ''
            )

            review.product = product
            if customer:
                order = Order.objects.filter(
                    customer=customer, items__product=product
                ).last()
                review.order = order
            review.save()
            messages.success(
                request, 'Review added successfully!', extra_tags="review"
            )
        else:
            messages.error(
                request, 'Failed to add review. Please check the form.'
            )

    return redirect(reverse(
        'product_detail', args=[product.id]  # type: ignore
    ))

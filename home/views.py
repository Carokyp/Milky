from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect


def index(request):
    """View to return the index page """
    return render(request, 'home/index.html')

# TODO: Remove test views before deployment


def test_success(request):
    messages.success(request, "Product added to your cart!")
    return redirect('home')


def test_warning(request):
    messages.warning(request, "This is a warning!")
    return redirect('home')


def test_error(request):
    messages.error(request, "Something went wrong!")
    return redirect('home')


def test_info(request):
    messages.info(request, "This is an info message!")
    return redirect('home')

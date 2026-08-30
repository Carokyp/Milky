from django.shortcuts import render

# Project-wide error handlers. Django looks these up via the
# handler404 / handler403 / handler405 / handler500 names set in milky/urls.py.


def handler404(request, exception):
    """Render the custom 404 error page."""
    return render(request, "errors/404.html", status=404)


def handler403(request, exception):
    """Render the custom 403 error page."""
    return render(request, "errors/403.html", status=403)


def handler405(request, exception):
    """Render the custom 405 error page."""
    return render(request, "errors/405.html", status=405)


def handler500(request):
    """Render the custom 500 error page."""
    return render(request, "errors/500.html", status=500)

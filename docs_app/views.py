from django.shortcuts import redirect

def redirectToIndex(request):
    """
    Redirects to the docs index if no file is specified.
    """
    return redirect('index.html')
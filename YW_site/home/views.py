from django.shortcuts import render

# Create your views here.
def render_login(request):
    return render(request, 'Login.html', {})

def render_landing_page(request):
    return render(request, 'LandingPage.html', {})
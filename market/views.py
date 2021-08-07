from django.shortcuts import redirect, render
from .forms import ContactForm
from django.contrib.auth.decorators import login_required



def home_page(request):
    context = { 'title':'Hello world! It is home page!',
            'content': 'Welcome to the homepage',
            'premium':'YEAHHHHH'}
    return render(request, 'home_page.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = { 'title':'Contact page!',
            'content': 'Welcome to the contactpage',
            'form': contact_form}
    
    if contact_form.is_valid():
        print(contact_form.cleaned_data['fullname'])
        print(contact_form.cleaned_data['email'])
        print(contact_form.cleaned_data['content'])
        
    return render(request, 'contact/view.html', context)


def about_page(request):
    context = { 'title':'About page!!',
            'content': 'Welcome to the aboutpage'}
    return render(request, 'home_page.html', context)
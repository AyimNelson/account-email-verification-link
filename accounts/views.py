from django.shortcuts import render

# Create your views here.
from .forms import SignupForm
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, logout, authenticate  
from django.utils.encoding import force_bytes, force_str    
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode  
from django.core.mail import EmailMessage  
from .tokens import account_activation_token  
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model 

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html', {})


  
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # the form has to be saved in the memory and not in DB
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            #This is  to obtain the current cite domain   
            current_site_info = get_current_site(request)  
            mail_subject = 'The Activation link has been sent to your email address'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site_info.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please proceed confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form}) 



def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # Can return render and html template 
    else:  
        return HttpResponse('Activation link is invalid!')
        # Can return render and html template
    
    
# Not in use...    
# def logout(request):
#     logout(request)  #recursion occuring....
#     return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
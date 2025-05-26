from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .decorators import custom_login_required
import logging


logger = logging.getLogger(__name__)

@login_required(login_url='customer_login')
def myAccount(request):
    return render(request, 'users/my_account.html', {
        'user': request.user,
    })

def activate(request, uidb64, token):              
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('customer_login') 
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('customer_login') 


def send_verification_email(request, user, mail_subject, email_template):
    """Function to send an email verification link"""
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.content_subtype = "html"
    email.send()

def admin_registration(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            profile_picture = request.FILES.get('profile_picture')

            
            logger.debug(f"Received Data: {email}, {username}, {first_name}, {last_name}")

            
            if not email or not password or not username:
                return JsonResponse({'success': False, 'error': 'Missing required fields.'})

            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture
            )

            
            user.is_staff = True 
            user.is_superuser = True 
            user.user_type = 'admin'  
            user.save()

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

            return JsonResponse({
                'success': True, 
                'message': 'Registration successful!', 
                'redirect_url': '/admin/login/'
            })

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
 
    return render(request, 'users/admin_registration.html')


def customer_registration(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            profile_picture = request.FILES.get('profile_picture')  


            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                profile_picture=profile_picture,
            )
            user.is_active = False 
            user.user_type = 'customer' 
            user.save()

            mail_subject = 'Activate your account'
            email_template = 'users/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            return JsonResponse({'success': True, 'message': 'Registration successful!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    return render(request, 'users/customer_registration.html')


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.user_type == 'customer': 
                login(request, user)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": True, "redirect_url": "/users/myAccount/"})
                else:
                    return redirect('myAccount')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": "Only customers are allowed to log in."})
                else:
                    messages.error(request, "Only customers are allowed to log in.")
                    return redirect('customer_login')

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "Invalid email or password."})
            else:
                messages.error(request, "Invalid email or password")
                return redirect('customer_login')

    return render(request, 'users/customer_login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('home')
    add_never_cache_headers(response)
    return response
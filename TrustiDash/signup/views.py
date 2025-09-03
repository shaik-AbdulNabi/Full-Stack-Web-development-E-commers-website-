from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from tdapp.models import *

# from this to generate_token are used for forgot password code
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

import secrets

def generate_token():
    return secrets.token_urlsafe(32)


# Create your views here.
def s(request):
    user = User.objects.get(user_name="harsha")
    h=user.user_password
    return render(request,'s.html',{'h':h})

def discount(op, dp):
    return op - (op * dp / 100)

def main(request):
    products=Product.objects.all()
    product_data = []
    for p in products:
        discounted_price  = discount(p.product_price,p.product_discount)
        product_data.append(
            {
            'id': p.id,
            'name': p.product_name,
            'price': p.product_price,
            'discount': p.product_discount,
            'discounted_price': round(discounted_price, 2),
            'quantity': p.product_quantity,
            'brand': p.product_brand,
            'category': p.product_category,
            'imageurl': p.product_url,
            }
        )
    return render(request,'main.html',{'h':product_data})


def sinoutf(request):
    # Always initialize both forms
    signup_form = UserForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = UserForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, "Registration successful. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the sign-up form.")

        elif 'signin' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                aupass = login_form.cleaned_data['password']
                autype = login_form.cleaned_data['user_type']

                if autype == "user":
                    try:
                        user = User.objects.get(user_name=name)
                    except User.DoesNotExist:
                        messages.error(request, "User not found.")
                        return redirect('login')

                    if aupass == user.user_password:
                        request.session['user_id'] = user.id
                        messages.success(request, "Login successful.")
                        return redirect('uhome')
                    else:
                        messages.error(request, "Password incorrect.")
                        return redirect('login')

                else:
                    try:
                        admin = Admin.objects.get(admin_name=name)
                    except Admin.DoesNotExist:
                        messages.error(request, "User not found.")
                        return redirect('login')

                    if aupass == admin.admin_password:
                        request.session['admin_id'] = admin.id
                        messages.success(request, "Login successful.")
                        return redirect('ahome')
                    else:
                        messages.error(request, "Password incorrect.")
                        return redirect('login')
            else:
                messages.error(request, "Please correct the login form.")

    return render(request, 'sinout.html', {'form': login_form, 'form1': signup_form})



def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(user_email=email)
                token = generate_token()
                # the below line is to save the forgot password token in PasswordResetToken table
                PasswordResetToken.objects.create(user=user, token=token)
                # ✅ Use reverse to generate the correct URL under /login/
                reset_link = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'token': token})
                )

                # Send Email
                subject = "Your Password Reset Link"
                message = f"Hi {user.user_name},\n\nClick to reset: {reset_link}"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

                return HttpResponse("Reset link sent to your email.")
            except User.DoesNotExist:
                return HttpResponse("Email not registered.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'forget_password/forgot_password.html', {'form': form})

def reset_password(request, token):
    try:
        # the below line checks the reset token in PasswordResetToken table 
        reset_entry = PasswordResetToken.objects.get(token=token)
        if not reset_entry.is_valid():
            return HttpResponse("Token expired")

        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_pass = form.cleaned_data['new_password']
                reset_entry.user.user_password = new_pass  # 🔒 hash this
                reset_entry.user.save()
                reset_entry.delete()
                return HttpResponse("Password reset successfully")
        else:
            form = ResetPasswordForm()

        return render(request, 'forget_password/reset_password.html', {'form': form})
    except PasswordResetToken.DoesNotExist:
        return HttpResponse("Invalid or expired token")




def logout(request):
    request.session.flush()  # Removes all session data
    return redirect('/')


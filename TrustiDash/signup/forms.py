
from django import forms
from tdapp.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_name',
            'user_password',
            'user_email',
            'user_phno',
            'user_pincode',
            'user_country',
            'user_state',
            'user_mundale',
            'user_city_or_village',
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'name': 'user_name'}),
            'user_password': forms.TextInput(attrs={'placeholder': 'Enter your password', 'name': 'user_password'}),
            'user_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'name': 'user_email'}),
            'user_phno': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'name': 'user_phno'}),
            'user_pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode', 'name': 'user_pincode'}),
            'user_country': forms.TextInput(attrs={'placeholder': 'Enter country', 'name': 'user_country'}),
            'user_state': forms.TextInput(attrs={'placeholder': 'Enter state', 'name': 'user_state'}),
            'user_mundale': forms.TextInput(attrs={'placeholder': 'Enter mundale', 'name': 'user_mundale'}),
            'user_city_or_village': forms.TextInput(attrs={'placeholder': 'Enter city or village', 'name': 'user_city_or_village'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # All fields are required
            field.label = ''       # No labels


class UserForm1(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'user_name',
            'user_password',
            
            'user_email',
            'user_phno',
            'user_pincode',
            'user_country',
            'user_state',
            'user_mundale',
            'user_city_or_village',
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'user_password': forms.TextInput(attrs={'placeholder': 'Enter your password'}),
           
            'user_email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'user_phno': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'user_pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode'}),
            'user_country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
            'user_state': forms.TextInput(attrs={'placeholder': 'Enter state'}),
            'user_mundale': forms.TextInput(attrs={'placeholder': 'Enter mundale'}),
            'user_city_or_village': forms.TextInput(attrs={'placeholder': 'Enter city or village'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # Make all fields required
            field.label = ''  # Hide label


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [
            'admin_name',
            'admin_password',
            'admin_shopname',
            'admin_email',
            'admin_phno',
            'admin_pincode',
            'admin_country',
            'admin_state',
            'admin_mundale',
            'admin_city_or_village',
        ]
        widgets = {
            'admin_password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'admin_name': forms.TextInput(attrs={'placeholder': 'Enter admin name'}),
            'admin_shopname': forms.TextInput(attrs={'placeholder': 'Enter shop name'}),
            'admin_email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'admin_phno': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'admin_pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode'}),
            'admin_country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
            'admin_state': forms.TextInput(attrs={'placeholder': 'Enter state'}),
            'admin_mundale': forms.TextInput(attrs={'placeholder': 'Enter mundale'}),
            'admin_city_or_village': forms.TextInput(attrs={'placeholder': 'Enter city or village'}),
        }

    # Enforce all fields as required
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class LoginForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'id': 'user_type_radio'  # This will be overridden in template if needed
        }),
        initial='user',
        label=''
    )

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'name': 'username',
        }),
        label=''
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'name': 'password',
        }),
        label=''
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Enter your Email",
        max_length=150,
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com',
            'class': 'form-control',
            'required': 'required'
        })
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password',
            'class': 'form-control',
            'required': 'required'
        })
    )


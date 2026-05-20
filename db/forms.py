from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,Order,Item

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    pan_number = forms.CharField(max_length=20, required=True)
    gst_number = forms.CharField(max_length=20, required=True)
    theme = forms.ChoiceField(
        choices=[(False,"Light"),(True,"Dark")],
        widget=forms.RadioSelect,
        required=True)
    pfp = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'password1', 
            'password2',
            'phone',
            'address',
            'pan_number',
            'gst_number',
            'pfp',
            'theme'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'address':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})           
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data['phone'],
                    'address': self.cleaned_data['address'],
                    'pan_number': self.cleaned_data['pan_number'],
                    'gst_number': self.cleaned_data['gst_number'],
                    'pfp': self.cleaned_data['pfp'],
                    'theme': self.cleaned_data['theme']
                }
            )
        return user
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    theme = forms.ChoiceField(
        choices=[(False, "Light"), (True, "Dark")],
        widget=forms.RadioSelect
    )
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'pan_number', 'gst_number', 'pfp','theme']   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'address':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'price', 'quantity', 'location', 'phone', 'order_type']
        widgets = {
            'location': forms.Textarea(attrs={'rows': 3}),
            'order_type': forms.RadioSelect(choices=[(True, 'Buy'), (False, 'Sell')]),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
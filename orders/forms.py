from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
 'postal_code', 'city']
        
class OrderForm(forms.Form):
    choices = [
        ('unfullfilled', 'Unfullfilled'),
        ('ready to pickup', 'READY TO PICKUP'),
        ('canceled', 'CANCELED'),
        ('shipped', 'SHIPPED'),
        ('partially fulfilled', 'PARTIALLY FULFILLED'),
        ('fullfilled', 'Fullfilled'),
    ]

    deliver = [
        ('Standard shipping', 'Standard shipping'),
        ('Local pickup', 'Local pickup'),
        ('Local delivery', 'Local delivery'),
        ('Free shipping', 'Free shipping'),
        ('Cash on delivery', 'Cash on delivery'),
        ('Express', 'Express'),
    ]
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        )
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Postal Code",
                "class": "form-control"
            }
        )
    )
    delivery = forms.ChoiceField(choices=deliver, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
    }), required=True)
    
    status = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
    }), required=True)
    
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "City",
                "class": "form-control"
            }
        )
    )
    paid = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        initial=False
    )
    

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
 'postal_code', 'city', 'delivery', 'status']
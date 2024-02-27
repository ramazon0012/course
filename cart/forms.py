from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=True, 
        widget=forms.TextInput(
            attrs = {
                "placeholder" : "Add to cart",
                "class" : "btn btn-lg btn-warning rounded-pill w-100 fs-9 fs-sm-8",
            }
        ))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
class QuantityUpdateForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control text-center input-spin-none bg-transparent border-0 px-0'}),
        min_value=1
    )
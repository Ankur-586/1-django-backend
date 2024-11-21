from django import forms
from .models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order_id', 'variant_id', 'quantity', 'price']
        widgets = {
            'price': forms.HiddenInput(),  # Hide price field from the admin form
        }

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Set price based on the variant
            if self.instance.variant_id:
                self.fields['price'].initial = self.instance.variant_id.price
        else:
            self.fields['price'].initial = 0

    def clean(self):
        cleaned_data = super(OrderItemForm, self).clean()
        variant = cleaned_data.get('variant_id')
        if variant:
            cleaned_data['price'] = variant.price
        return cleaned_data

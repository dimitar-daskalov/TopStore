from django import forms

from TopStore.shared.bootstrap_form_mixin import BootstrapFormMixin
from TopStore.store.models import ContactMessage, OrderInformation


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'


class OrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OrderInformation
        fields = '__all__'
        widgets = {
            'order': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'address': forms.TextInput(attrs={'placeholder': 'Address...'}),
            'city': forms.TextInput(attrs={'placeholder': 'City...'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip code...'}),
            'telephone_number': forms.TextInput(attrs={'placeholder': 'Phone number...'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comment...'}),
        }

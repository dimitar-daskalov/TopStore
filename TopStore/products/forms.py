from django import forms

from TopStore.products.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)


class ReviewForm(forms.ModelForm):
    product_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Review
        fields = ('text', 'product_pk')

    def save(self, commit=True):
        product_pk = self.cleaned_data['product_pk']
        product = Product.objects.get(pk=product_pk)
        review = Review(
            text=self.cleaned_data['text'],
            product=product,
        )

        if commit:
            review.save()

        return review

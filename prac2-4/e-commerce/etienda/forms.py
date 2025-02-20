from django import forms

# Define las opciones para el campo "category"
CATEGORIES = (
    ("women's clothing", "Women's fashion"),
    ("men's clothing", "Men's fashion"),
    ('jewelery', 'Jewelery'),
    ('electronics', 'Electronics'),
)

class ProductForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=CATEGORIES)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    image = forms.ImageField()
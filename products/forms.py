from django import forms
from .models import Product, SubCategory, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        subcategory = SubCategory.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) fpr c om categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, SubCategory, Category, Review




class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subcategories = SubCategory.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in subcategories]

        self.fields['subcategory'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating', 'comment',)
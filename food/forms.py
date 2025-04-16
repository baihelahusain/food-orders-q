from django import forms 
from .models import Item 

class ItemForm(forms.ModelForm):
    Item_name = forms.CharField(
        label="Item Name",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter item name',
            'autofocus': True
        }),
        help_text="Enter the name of your food item"
    )
    
    Item_desc = forms.CharField(
        label="Description",
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your food item',
            'rows': 3
        }),
        help_text="Provide a detailed description of the item"
    )
    
    Item_price = forms.IntegerField(
        label="Price ($)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter price',
            'min': 0
        }),
        help_text="Enter the price in dollars (whole numbers only)"
    )
    
    Item_img = forms.CharField(
        label="Image URL",
        max_length=1100,
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter image URL'
        }),
        help_text="Paste a URL to an image of your food item (leave empty for default image)"
    )
    
    class Meta:
        model = Item
        fields = ['Item_name', 'Item_desc', 'Item_price', 'Item_img']
    
    def clean_Item_price(self):
        price = self.cleaned_data.get('Item_price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price
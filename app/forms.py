from .models import *
from django import forms
from django.forms.models import inlineformset_factory
from datetime import datetime,date
import re
style={'text': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
       'image':'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
      'checkbox':'w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800', 
      }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['first_name','last_name','image','phone_number','city','address']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
    def clean_phone_number(self):
        m=self.cleaned_data.get('phone_number')
        if re.match(r'^\d{10}$',m):
            return m
        else:
            raise forms.ValidationError("Enter valid number")
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','category','description','image','quantity','price',"gender",'rent_method','availability','period','location']
        widgets = {
            'period': forms.DateInput(attrs={'type': 'date',}),
        }
        # 'min': date.today().strftime('%Y-%m-%d')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
    def clean_price(self):
        m=self.cleaned_data.get('price')
        if m>0:
            return m
        else:
            raise forms.ValidationError("Price should be greater than 0")
    def clean_quantity(self):
        m=self.cleaned_data.get('quantity')
        if m>=0:
            return m
        else:
            raise forms.ValidationError("Quantity should be negative")
        # self.fields["period"].widget.attrs.update({"type":"date"})
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment','image','rating']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})    
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['subject','comment','image','rating']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})    
class MakeOrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['rent_start','rent_end',"delivery_type",'full_name','mobile_no','alternate_no','pin_code','address']
        widgets = {
            'rent_start': forms.DateInput(attrs={'type': 'date','min': date.today().strftime('%Y-%m-%d'),"class":style["text"]}),
            'rent_end': forms.DateInput(attrs={'type': 'date','min': date.today().strftime('%Y-%m-%d'),"class":style["text"]}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
    def clean_mobile_no(self):
        m=self.cleaned_data.get('mobile_no')
        if re.match(r'^\d{10}$',m):
            return m
        else:
            raise forms.ValidationError("Enter valid number")
    def clean_pin_code(self):
        m=self.cleaned_data.get('pin_code')
        if re.match(r'^\d{6}$',m):
            return m
        else:
            raise forms.ValidationError("Enter valid pin code")
    def clean_alternate_no(self):
        m=self.cleaned_data.get('alternate_no')
        if re.match(r'^\d{10}$',m):
            return m
        else:
            raise forms.ValidationError("Enter valid number")
    def clean_rent_start(self):
        start_date = self.cleaned_data.get('rent_start')
        if start_date < date.today():
            raise forms.ValidationError("Start date must be greater than today's date.")
        return start_date
    def clean_rent_end(self):
        end_date = self.cleaned_data.get('rent_end')
        start_date = self.cleaned_data.get('rent_start')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be later than the start date.")
        return end_date
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['delivery_date','delivery_status']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date',}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
class SliderForm(forms.ModelForm):
    class Meta:
        model=Slider
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class':style['image']})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class':style['text'],'rows':3})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class':style['checkbox']})
            else:
                field.widget.attrs.update({'class':style['text']})
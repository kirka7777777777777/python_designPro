from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 2MB')
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise forms.ValidationError('Допустимые форматы: JPG, JPEG, PNG, BMP')
        return image
from django import forms
from .models import Application, Category


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 2MB')
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise forms.ValidationError('Допустимые форматы: JPG, JPEG, PNG, BMP')
        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'comment', 'design_image']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('comment')
        design_image = cleaned_data.get('design_image')

        if status == 'in_progress' and not comment:
            raise forms.ValidationError('При принятии в работу обязателен комментарий')

        if status == 'completed' and not design_image:
            raise forms.ValidationError('При завершении заявки обязательно изображение дизайна')

        return cleaned_data
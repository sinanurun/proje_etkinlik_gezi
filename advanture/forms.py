from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm, TextInput, FileInput, Select

from advanture.models import Advanture, Category, Location


class AdvantureForm(ModelForm):
    class Meta:
        model = Advanture

        fields = ['category', 'location', 'title', 'keywords', 'description', 'image',
                  'price', 'day', 'detail', 'slug']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'Category'}, choices=Category.objects.all()),
            'location': Select(attrs={'class': 'input', 'placeholder': 'Location'}, choices=Location.objects.all()),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Image', }),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'Price'}),
            'day': TextInput(attrs={'class': 'input', 'placeholder': 'Day'}),
            'detail': CKEditorUploadingWidget(),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
        }


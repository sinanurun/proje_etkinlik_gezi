from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Create your models here.


# advanture kategorileri için
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Location(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


# advanture için

class Advanture(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )



    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    day = models.IntegerField(default=0)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    advanture = models.ForeignKey(Advanture, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="250"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""

    def __str__(self):
        return self.title


class AdvantureForm(ModelForm):
    class Meta:
        model = Advanture

        fields = ['category', 'location', 'title', 'keywords', 'description', 'image', 'price', 'day','detail', 'slug']
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


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    advanture = models.ForeignKey(Advanture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

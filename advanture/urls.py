from django.urls import path

from . import views

urlpatterns = [
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]
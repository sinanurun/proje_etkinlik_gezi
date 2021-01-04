from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from advanture.models import Category, Advanture, Images, Comment, CommentForm
from home.models import Setting


def category_advantures(request, id, slug):
    catdata = Category.objects.get(pk=id)
    advantures = Advanture.objects.filter(category_id=id,status=True)  # default language
    category = Category.objects.all()
    context = {'advantures': advantures,
               'category': category,
               'catdata': catdata}
    return render(request, 'category.html', context)


def advanture_details(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(status=True).all()
    advanture = Advanture.objects.get(pk=id)  # default language
    images = Images.objects.filter(advanture=id).all()
    comments = Comment.objects.filter(advanture=id, status=True).all()

    context = {'setting': setting,
               'advanture': advanture,
               'comments': comments,
               'images': images,
               'category': category}
    return render(request, 'advanture_details.html', context)

def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.advanture_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)
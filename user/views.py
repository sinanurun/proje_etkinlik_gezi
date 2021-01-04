from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


from advanture.models import Advanture, Category, AdvantureForm, Comment
from home.models import Setting
from user.forms import UserUpdateForm, ProfileUpdateForm, SignUpForm
from user.models import UserProfile


@login_required(login_url='/login')  # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'profile': profile,
               'setting':setting}
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        setting = Setting.objects.get(pk=1)
        context = {
            'category': category,
            'setting':setting,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        setting = Setting.objects.get(pk=1)
        return render(request, 'user_password.html', {'form': form, 'category': category,'setting':setting})


@login_required(login_url='/login')  # Check login
def user_advantures(request):
    category = Category.objects.all()
    current_user = request.user
    advantures = Advanture.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'setting':setting,
               'advantures': advantures, }
    return render(request, 'user_advantures.html', context)


@login_required(login_url='/login')  # Check login
def user_advantures_add(request):
    if request.method == 'POST':
        form = AdvantureForm(request.POST, request.FILES)

        if form.is_valid():
            current_user = request.user
            data = Advanture()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.detail = form.cleaned_data['detail']
            data.category = form.cleaned_data['category']
            data.STATUS = 'False'

            data.location = form.cleaned_data['location']
            data.price = form.cleaned_data['price']
            data.day = form.cleaned_data['day']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.slug = form.cleaned_data['slug']
            data.save()
            messages.success(request,"Your Advanture is Added")
            return HttpResponseRedirect('/user/user_advantures')
        else:
            messages.success(request, "Advanture Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/user_advantures')


    form = AdvantureForm
    category = Category.objects.all()
    current_user = request.user
    advantures = Advanture.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'advantures': advantures,
               'setting':setting,
               'form': form,
               }
    return render(request, 'user_advanture_add.html', context)



@login_required(login_url='/login')  # Check login
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'category': category,
        'comments': comments,
        'setting':setting,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check login
def user_delete_advanture(request, id):
    current_user = request.user
    Advanture.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Advanture deleted..')
    return HttpResponseRedirect('/user/user_advantures')


@login_required(login_url='/login')  # Check login
def user_update_advanture(request, id):
    advanture = Advanture.objects.get(id=id)
    if request.method == 'POST':
        form = AdvantureForm(request.POST, request.FILES, instance=advanture)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Advanture ise Updateded")
            return HttpResponseRedirect('/user/user_advantures')
        else:
            messages.success(request, "Advanture Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/user_advantures')

    form = AdvantureForm(instance=advanture)
    category = Category.objects.all()
    current_user = request.user
    advantures = Advanture.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'setting':setting,
               'advantures': advantures,
               'form': form,
               }
    return render(request, 'user_advanture_update.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, 'signin.html', context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'form': form}

    return render(request, 'signup.html', context)

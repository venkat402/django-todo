from django.core.exceptions import ValidationError
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Task
import datetime
from datetime import datetime
from django import template
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# login stuff
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    data = Task.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'index.html', context={'key': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        task_data = request.POST.dict()
        if not task_data.get("task_name"):
            messages.error(request, 'Task name is required.')
            return HttpResponseRedirect('/')
        obj = Task()
        obj.task_name = task_data.get("task_name")
        obj.task_status = 'pending'
        obj.save()
        messages.success(request, 'Form successfully saved.')
        return HttpResponseRedirect('/')

@login_required
def change_status(request, id):
    data = Task.objects.get(pk=id)
    if data.task_status == 'pending':
        data.task_status = 'completed'
        data.save()
    else:
        data.task_status = 'pending'
        data.save()
    messages.success(request, 'Status changed successfully.')
    return HttpResponseRedirect('/')

@login_required
def delete_task(request, id):
    data = Task.objects.get(pk=id).delete()
    messages.success(request, 'Task deleted successfully.')
    return HttpResponseRedirect('/')

@login_required
def update_task(request, id):
    if request.method == 'POST':
        task_data = request.POST.dict()
        if not task_data.get("task_name"):
            messages.error(request, 'Task name is required.')
            return HttpResponseRedirect('')
        obj = Task.objects.get(pk=id)
        obj.task_name = task_data.get("task_name")
        obj.save()
        messages.success(request, 'Update saved successfully.')
        return HttpResponseRedirect('/')

    data = Task.objects.get(pk=id)
    context = {
        'task_data': data,
        'update': True,
        'id': id
    }
    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html')




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def user_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


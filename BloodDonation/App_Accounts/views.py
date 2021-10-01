from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from App_Accounts.forms import *


def Signupview(request):
    if request.user.is_authenticated:
        return redirect('App_Blood:index')
    else:
        try:
            if request.method == "POST":
                form = SignUpForm(request.POST or None)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.profile.type = form.cleaned_data.get('type')
                    user.save()
                    messages.success(request, "Signup Done,Please Login to Complete your Profile",
                                     extra_tags="signup_complete")
                    return redirect(request.POST['next'])
            else:
                form = SignUpForm()
        except:
            return redirect('App_Accounts:signup')

        context = {
            'form': form,
        }
        return render(request, 'App_Accounts/signuppage.html', context)


def Loginview(request):
    if request.user.is_authenticated:
        return redirect('App_Blood:index')
    else:
        if request.method == "POST":
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            next = request.GET.get("next", '')
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                if next != "":
                    return redirect(next)
                return redirect('App_Accounts:dashboard')
            else:
                messages.info(request, "Enter correct username and password", extra_tags="login_error")
                return redirect('App_Accounts:login')
        else:
            return render(request, 'App_Accounts/login.html')


@login_required(login_url='App_Accounts:login')
def Logoutview(request):
    logout(request)
    return redirect('App_Accounts:login')


@login_required(login_url='App_Accounts:login')
def Dashboard(request):
    return render(request, 'App_User/index.html')


@login_required(login_url='App_Accounts:login')
def Profileupdate(request):
    try:
        if request.method=="POST":
            form=ProfileUpdateForm(request.POST or None,request.FILES,instance=request.user.profile)
            form_2=UserUpdateForm(request.POST or None,instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request,"Profile Update successfully",extra_tags="profile_update")
                return redirect(request.POST['next'])
        else:
            form=ProfileUpdateForm(instance=request.user.profile)
            form_2 = UserUpdateForm(instance=request.user)
    except:
        return redirect('App_Accounts:dashboard')

    context={
        'form':form,
        'form_2':form_2,
    }
    return render(request, 'App_User/updateprofile.html',context)


@login_required(login_url="App_Accounts:login")
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags="pass_change")
            return redirect('App_Accounts:passwordchange')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'App_User/change_password.html', {
        'form': form
    })

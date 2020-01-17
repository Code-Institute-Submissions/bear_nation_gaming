from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             authenticated_user = authenticate(username=new_user.username,
#                                               password=request.POST['password1'])
#             login(request, authenticated_user)
#             return HttpResponseRedirect(reverse('home'))
#     else:
#         form = UserCreationForm()
#
#     context = {'form': form}
#     return render(request, 'users/register.html', context)

# Registration View
def register(request):
    """ Render the registration page """
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                return redirect(reverse('home'))
                messages.success(request, "You have successfully registered")
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'users/register.html', {"registration_form": registration_form})


# Login View
def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

        # Code to allow users to login with both username/email was adapted from https://www.youtube.com/watch?v=c7PqMsQiWKU
        try:
            user = auth.authenticate(username=User.objects.get(email=username), password=password)
        except:
            user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(user=user, request=request)
            messages.success(request, "You have successfully logged in!")
            return redirect(reverse('home'))
        else:
            login_form.add_error(None, "Your username or password is incorrect")

    else:
        login_form = UserLoginForm()
    return render(request, 'users/login.html', {'login_form': login_form})


@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('logout'))
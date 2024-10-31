# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import UserData
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:   
            # Optional: Display the form errors if the form is not valid
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()  # Initialize an empty form for GET requests

    return render(request, 'myapp/register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('user_data')
#     else:
#         form = UserLoginForm()
#     return render(request, 'myapp/login.html', {'form': form})

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def user_login(request):
    username_error = ""
    password_error = ""
    create_account_error = ""
    user = None  # Initialize user to prevent UnboundLocalError

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate username and password
        if not username and not password:
            username_error = "Please enter an email address."
            password_error = "Please enter a password."
        elif not username:
            username_error = "Please enter an email address."
        elif not password:
            if '@' not in username:
                username_error = "Please enter a valid email address."
            else:
                password_error = "Please enter Password."
        elif '@' not in username:
            username_error = "Please enter a valid email address."

        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/data/'})  # Adjust the URL
            else:
                password_error = "Incorrect password."

        # If we reach this point, the user is None, handle error responses
        return JsonResponse({
            'success': False,
            'username_error': username_error,
            'password_error': password_error,
        })

    # Handle account creation message when redirected from the register page
    if request.GET.get('error') == 'account_exists':
        create_account_error = "You are already registered. Please log in to continue."

    return render(request, 'myapp/login.html', {
        'username_error': username_error,
        'password_error': password_error,
        'create_account_error': create_account_error,
    })




# @login_required
# def user_data(request):
#     data = UserData.objects.filter(user=request.user)
#     return render(request, 'myapp/user_data.html', {'data': data})\

@login_required
def user_data(request):
    data = UserData.objects.filter(user=request.user)  # Fetch data for the logged-in user
    return render(request, 'myapp/user_data.html', {'data': data})




@login_required
def add_data(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST['gender']
        weight = request.POST['weight']
        height = request.POST['height']
        food_type = request.POST['food_type']
        user_data = UserData(user=request.user, name=name, email=email, dob=dob, gender=gender, weight=weight, height=height, food_type=food_type)
        user_data.save()
        return redirect('user_data')
    return render(request, 'myapp/add_data.html')

from django.shortcuts import render
from .models import UserData

def edit_data(request, pk):
    data = UserData.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.dob = request.POST['dob']
        data.gender = request.POST['gender']
        data.weight = request.POST['weight']
        data.height = request.POST['height']
        data.food_type = request.POST['food_type']
        data.save()
        return redirect('user_data')
    
    # Format date for input field
    formatted_dob = data.dob.strftime('%Y-%m-%d') if data.dob else ''
    return render(request, 'myapp/edit_data.html', {'data': data, 'formatted_dob': formatted_dob})

@login_required
def delete_data(request, pk):
    data = UserData.objects.get(pk=pk, user=request.user)
    data.delete()
    return redirect('user_data')

def user_logout(request):
    logout(request)
    return redirect('login')

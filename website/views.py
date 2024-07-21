from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.utils.safestring import mark_safe

def home(request):
    records = Record.objects.all()
    # Login Logic
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(
                request, ("Error logging in, please try again..."))
            return redirect('home')
    else:
        return render(request, "home.html", {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully!"))
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form':form})
    return render(request, "register.html", {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {'customer_record':customer_record})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        first_name = delete_it.first_name
        last_name = delete_it.last_name
        delete_it.delete()
        messages.success(request, mark_safe(f"Record for <b>{first_name} {last_name}</b> successfully deleted!"))
        return redirect('home')
    else:
        messages.success(request, ("You must be logged in to do that..."))
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                first_name = add_record.first_name
                last_name = add_record.last_name
                messages.success(request, mark_safe(f"User <b>{first_name} {last_name}</b> successfully added!"))
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')

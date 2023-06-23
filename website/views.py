from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Record

def home(request):
   records=Record.objects.all()
   context = {
        'records': records,
    }
   
   return render(request, "home.html", context)


def index(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']

      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect('home')
      else:
         messages.success(request, "ERROR, Please Try Again...")
         return redirect('index')
   else:
      return render(request, "index.html", {})


def register(request):
    title = 'Create an account'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and email and password1 and password2):
            error_msg = 'Please fill out all fields'
            return render(request, 'register.html', {'title': title, 'error_msg': error_msg})

        if password1 != password2:
            error_msg = 'Passwords do not match'
            return render(request, 'register.html', {'title': title, 'error_msg': error_msg})

        if User.objects.filter(username=username).exists():
            error_msg = 'Username is taken'
            return render(request, 'register.html', {'title': title, 'error_msg': error_msg})
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()
        
        return redirect('index')
    else:
        return render(request, 'register.html', {'title': title})


def customer_record(request, pk):
   if request.user.is_authenticated:
       customer_record =Record.objects.get(passport_no=pk) 
       context = {
           'customer_record': customer_record,
        }
       return render(request, "record.html", context)

def customer_delete(request, pk):
    if request.user.is_authenticated:
       delete_it =Record.objects.get(passport_no=pk) 
       delete_it.delete()
       
       return redirect('home')
 
def add_customer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Retrieve form data
            passport_no = request.POST['passport_no']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            city = request.POST['city']
            address = request.POST['address']
            zipcode = request.POST['zipcode']

            # Create a new Record instance
            record = Record(
                passport_no=passport_no,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                city=city,
                address=address,
                zipcode=zipcode
            )
            record.save()
            return redirect('home') 

        return render(request, 'add_customer.html')



def logout_view(request):
    logout(request)
    return redirect('/')
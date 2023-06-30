from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Record
from django.urls import reverse
import pandas as pd
import xlsxwriter
from django.http import HttpResponse
from io import BytesIO 

def home(request):
    record_list = Record.objects.all().order_by('-created_at')
    filter_option = request.GET.get('filter')
    if filter_option == '10':
        record_list = record_list[:10]  
    elif filter_option == '20':
        record_list = record_list[:20]
    elif filter_option == '30':
        record_list = record_list[:30]
    elif filter_option == 'All':
        pass  # Show all customers

    context = {
        'records': record_list,
        'filter_option': filter_option
    }

    return render(request, "home.html", context)


def index(request):
   record_list = Record.objects.all().order_by('-created_at')
   filter_option = request.GET.get('filter')
   if filter_option == '10':
       record_list = record_list[:10]  
   elif filter_option == '20':
        record_list = record_list[:20]
   elif filter_option == '30':
        record_list = record_list[:30]
   elif filter_option == 'All':
        pass  # Show all customers
   
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
      context = {
        'records': record_list,
        'filter_option': filter_option
    }
      return render(request, "index.html", context)


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
   try:
        if request.user.is_authenticated:
            customer_record =Record.objects.get(passport_no=pk) 
            context = {
                'customer_record': customer_record,
                }
            return render(request, "record.html", context)
   except:
        return render(request, "error.html")

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
            # Check if customer already exists
            if Record.objects.filter(passport_no=passport_no).exists():
                messages.error(request, 'Customer with this passport number already exists.')
            else:
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

def update_customer(request, pk):
    if request.user.is_authenticated:
        update_cust = get_object_or_404(Record, passport_no=pk)

        if request.method == 'POST':
            form_data = request.POST
            update_cust.passport_no = form_data['passport_no']
            update_cust.first_name = form_data['first_name']
            update_cust.last_name = form_data['last_name']
            update_cust.email = form_data['email']
            update_cust.phone = form_data['phone']
            update_cust.city = form_data['city']
            update_cust.address = form_data['address']
            update_cust.zipcode = form_data['zipcode']
            update_cust.save()

            
            return redirect(reverse('customer_record', args=[pk]))

        context = {
            'update_cust': update_cust
        }
        return render(request, 'update_customer.html', context)



def logout_view(request):
    logout(request)
    return redirect('/')

def export_to_excel(request):
    records = Record.objects.all()
    data = {
        'Passport No': [],
        'First Name': [],
        'Last Name': [],
        'Email': [],
        'Phone': [],
        'City': [],
        'Address': [],
        'Zipcode': []
    }

    for record in records:
        data['Passport No'].append(record.passport_no)
        data['First Name'].append(record.first_name)
        data['Last Name'].append(record.last_name)
        data['Email'].append(record.email)
        data['Phone'].append(record.phone)
        data['City'].append(record.city)
        data['Address'].append(record.address)
        data['Zipcode'].append(record.zipcode)

    df = pd.DataFrame(data)

    # Create a BytesIO buffer to hold the Excel file
    excel_buffer = BytesIO()

    # Create the Excel writer using xlsxwriter.Workbook
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        # Write the DataFrame to the Excel file
        df.to_excel(writer, index=False, sheet_name='Table Data')

    # Seek to the beginning of the buffer
    excel_buffer.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Customers_data.xlsx"'
    response.write(excel_buffer.getvalue())

    return response
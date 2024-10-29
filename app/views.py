from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import VaccinatedCow, PendingTask, MilkRecord
from datetime import datetime, date
from django.db.models import Sum
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages  # For flashing messages
from .sendMail import *
#########  LOGIN  ########

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Log in the user
            return redirect('dashboard')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'login.html')

########  SIGNUP  ###########
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Prepare the welcome email
            subject = "Welcome to Dairy Farmers!"
            message = f"""<p>Hi {username},</p>
                          <p>Thank you for signing up!</p>
                          <p>You can now explore Dairy Farmers services.</p>
                          <p>Best regards,<br>DairyFarmers Team</p>"""
            
            # Send the email with the image
            email_client.send_email(email, subject, message, image_path="./logo.png")

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('signup')

    return render(request, 'signup.html')



########  DASHBOARD  #########

@login_required
def dashboard(request):
    # Simulated data for milk usage and reminders
    milk_usages = [
        {'type': 'Whole Milk', 'used': 10, 'total': 135, 'usage_percentage': 10},
        {'type': '2% Milk', 'used': 0, 'total': 348, 'usage_percentage': 0},
        {'type': 'Skim (Nonfat) Milk', 'used': 10, 'total': 344, 'usage_percentage': 1},
        # Add more milk types if needed
    ]

    reminders = [
        "Reminder: Record today's milk gallon usage",
        "New Almond milk shipment coming in 2 days",
        # Add more reminders if needed
    ]

    context = {
        'user': request.user,
        'current_date': datetime.now().strftime('%A, %d %B, %Y'),
        'milk_usages': milk_usages,
        'reminders': reminders,
    }

    return render(request, 'dashboard.html', context)
####### VACINATION ####### 

def vacination(request):
    # Fetch all vaccinated cows from the database
    vaccinated_cows = VaccinatedCow.objects.all()
    pendingTask = PendingTask.objects.all()
    # Prepare context with the list of vaccinated cows
    context = {
        'vaccinated_cows': vaccinated_cows,
        'total_vaccinated':  len(vaccinated_cows),
        'pendingTask': len(pendingTask),
        'pending_tasks': pendingTask
    }
    
    return render(request, 'vacination.html', context)


def add_vaccination(request):
    if request.method == 'POST':
        cow_name = request.POST.get('cow_name')
        vaccine_date = request.POST.get('vaccine_date')

        # Validation (simple example)
        if cow_name and vaccine_date:
            # Create and save a new vaccinated cow record
            VaccinatedCow.objects.create(cow_name=cow_name, vaccine_date=vaccine_date)
            return redirect('vaccination')  # Redirect to the dashboard or another view
        else:
            return HttpResponse("Invalid data. Please provide both cow name and vaccination date.", status=400)

    # If GET request, just render the add_vaccination page
    return render(request, 'add_vaccination.html')

    

def add_pending_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        due_date = request.POST.get('due_date')
        
        # Create and save the new task
        new_task = PendingTask(task_name=task_name, due_date=due_date)
        new_task.save()
        
        return redirect('vaccination')  # Redirect to the dashboard after adding

    return render(request, 'add_pending_task.html')    

def report(request):
    # Fetch all data from the models
    pending_tasks = PendingTask.objects.all()
    milk_records = MilkRecord.objects.all()
    vaccinated_cows = VaccinatedCow.objects.all()
    
    context = {
        'pending_tasks': pending_tasks,
        'milk_records': milk_records,
        'vaccinated_cows': vaccinated_cows,
    }
    
    return render(request, 'reports.html', context)    


def logout_view(request):
    logout(request)
    return redirect('login')    

def milk_collection(request):
    if request.method == 'POST':
        cow_name = request.POST.get('cow_name')
        litres = request.POST.get('litres')
        delivery_date = request.POST.get('delivery_date')

        # Create a new milk record
        MilkRecord.objects.create(cow_name=cow_name, litres=litres, delivery_date=delivery_date)
        return redirect('milk-collection')  # Redirect to the same page after adding milk

    # Calculate totals
    total_milk_today = MilkRecord.objects.filter(delivery_date=date.today()).aggregate(Sum('litres'))['litres__sum'] or 0
    total_milk_month = MilkRecord.objects.filter(delivery_date__month=date.today().month).aggregate(Sum('litres'))['litres__sum'] or 0
    total_milk_year = MilkRecord.objects.filter(delivery_date__year=date.today().year).aggregate(Sum('litres'))['litres__sum'] or 0

    # Get all milk records
    milk_records = MilkRecord.objects.all()
    milk_trend_dates = ['2024-10-01', '2024-10-02', '2024-10-03']
    milk_trend_values = [45, 50, 40]

    context = {
        'total_milk_today': total_milk_today,
        'total_milk_month': total_milk_month,
        'total_milk_year': total_milk_year,
        'milk_records': milk_records,
        'milk_trend_dates': milk_trend_dates,
        'milk_trend_values': milk_trend_values
    }

    return render(request, 'milk_collection.html', context)


import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
# Configure the API key for authentication
genai.configure(api_key="AIzaSyDmVgtBtEqHyCPhEL4naok1ZjRdRmdB7iI")
model = genai.GenerativeModel('gemini-1.5-flash')


@csrf_exempt  # Use this only for testing; consider proper CSRF handling for production
def generate_text(request):
    if request.method == "POST":
        try:
            # Read the JSON body
            body = json.loads(request.body)
            user_input = body.get('user_input', '')
        except json.JSONDecodeError:
            return JsonResponse({'response_text': 'Invalid JSON'}, status=400)

        prompt = f"You are a helpful assistant for Dairy Farmers. Answer the following question: {user_input}"
        print(f"Prompt: {prompt}")

        # Generate content using the AI model
        response = model.generate_content(prompt)

        # Extract the text from the response
        try:
            response_text = response.candidates[0].content.parts[0].text
        except (IndexError, AttributeError):
            response_text = "Sorry, I couldn't generate a response."

        return JsonResponse({'response_text': response_text})

    return JsonResponse({'response_text': ''})
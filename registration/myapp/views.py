from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import CallAnalitics
from django.http import HttpResponse
from .models import Schedule
from .models import Data
import pandas as pd
import requests
import random
import time
import re

@login_required(login_url='login')
def BasePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        phone=request.POST.get('phone')
        pass1=request.POST.get('password1')
        my_user=User.objects.create_user(uname,phone,pass1)
        my_user.save()
        return redirect('home')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = 'Username or password is incorrect!'
            context = {
                'error_message': error_message,
                'username': username,
            }
            return render(request, 'login.html', context=context)
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def BasePage(request):
    return render(request, 'base.html')

def HomePage(request):
    return render(request, 'home.html')

def ContactsPage(request):
    return render(request, 'contacts.html')

def SchedulePage(request):
    return render(request, 'schedule.html')

def ScenarioPage(request):
    return render(request, 'scenario.html')

def create_call(request):
    url = request.POST.get('pbxinput')
    caller = '711007'
    password = '103103103'
    ext_id = 'Chrome_extension 11'
    user = 103
    app = 'Chrome extension'

    phone_numbers = Data.objects.values_list('phones', flat=True)

    call_ids = [random.randint(1000000000000000000, 9999999999999999999) for _ in range(len(phone_numbers))]

    responses = []

    for i in range(len(phone_numbers)):
        data = {
            'callid': call_ids[i],
            'caller': caller,
            'pass': password,
            'cmd': 0,
            'id': ext_id,
            'dest': phone_numbers[i],
            'user': user,
            'app': app
        }
        response = requests.post(url, data=data, verify=False)
        response_text = response.text.strip()
        state_pattern = re.compile(r'State=(\d+)')
        state_match = state_pattern.search(response_text)
        if state_match:
            state_code = int(state_match.group(1))
            if state_code == 5:
                responses.append("Extension Authorization Failed.")
            elif state_code == 18:
                responses.append("iQall Toggling License Failure.")
            elif state_code == 4:
                responses.append("Invalid Parameter.")
            elif state_code == 8:
                responses.append("Empty Destination Error!")
            elif state_code == 7:
                responses.append("Empty Caller Error!")
            elif state_code == 10:
                responses.append("Extension Access Temporarily Blocked!")
            elif state_code == 20:
                responses.append("Success! Response Code - " + str(state_code))
        else:
            responses.append("Error! Bad Response. Response Code - " + response_text)
        
        if i != len(phone_numbers)-1:
            time.sleep(5)

    return HttpResponse('<br>'.join(responses))


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                data, created = Data.objects.get_or_create(
                    name=row['Name'],
                    phones=row['Phones'],
                    date=row['Date'],
                    time=row['Time']
                )
                data.save()

                status_options = ["Answered", "Didn't Answer"]
                weights = [2, 1]
                call_analytics, created = CallAnalitics.objects.get_or_create(
                    name=row['Name'],
                    phones=row['Phones'],
                    date=row['Date'],
                    time=row['Time'],
                    status=random.choices(status_options, weights=weights)[0]
                )
                call_analytics.save()

            data = Data.objects.all()
            call_analytics = CallAnalitics.objects.all()

            return render(request, 'contacts.html', {"data": data, "call_analytics": call_analytics})
    return render(request, 'contacts.html')

def save_schedule(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')

        end_time = request.POST.get('end_time')
        max_number = request.POST.get('max_number')
        max_retry = request.POST.get('max_retry')
        time_between = request.POST.get('time_between')
        schedule = Schedule(start_time=start_time, end_time=end_time, number_calls=max_number,
                            retry_count=max_retry, repeated_time=time_between)
        schedule.save()
        return render(request, 'schedule.html')

def ConnectionPage(request):
    total_calls = CallAnalitics.objects.count()
    answered_calls = CallAnalitics.objects.filter(status="Answered").count()
    didnt_answer_calls = CallAnalitics.objects.filter(status="Didn't Answer").count()
    closed_calls = total_calls
    call_analytics = CallAnalitics.objects.all()
    return render(request, 'connection.html', {
        'total_calls': total_calls,
        'answered_calls': answered_calls,
        'didnt_answer_calls': didnt_answer_calls,
        'closed_calls': closed_calls,
        'call_analytics': call_analytics
    })


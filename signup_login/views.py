from django.contrib import messages
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect
from signup_login.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        user_type = request.POST.get('userType')
        address_line1 = request.POST.get('addressLine1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')

        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                address_line1=address_line1,
                city=city,
                state=state,
                pincode=pincode
            )
            if len(request.FILES)!=0:
                user.profile_picture=request.FILES['profilePicture']
            user.save()
            messages.success(request, "Signup successful! You can now log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "An error occurred while processing your request. Please try again.")
        except ValidationError as e:
            messages.error(request, str(e))
    
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_type'] = user.user_type

            if user.user_type == 'doctor':
                return HttpResponseRedirect(f'/doctor_dashboard/?user_id={user.id}')
            elif user.user_type == 'patient':
                return HttpResponseRedirect(f'/patient_dashboard/?user_id={user.id}')
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def doctor_dashboard(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return HttpResponseBadRequest("User ID is missing.")
    
    try:
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
         
        }
        return render(request, 'doctor_dashboard.html', context)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found.")


def patient_dashboard(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return HttpResponseBadRequest("User ID is missing.")
    
    try:
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
            
        }
        return render(request, 'patient_dashboard.html', context)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found.")
    
def logout(request):
    request.session.flush()
    return redirect('login')
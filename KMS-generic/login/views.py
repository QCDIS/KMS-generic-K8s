from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from users.models import UserProfile



def generate_schedule_list(duration, start_date_str, end_date_str):
    # Parse input dates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Define frequency delta based on duration
    frequency = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
        "monthly": "monthly",
        "yearly": "yearly",
        "once": None
    }
    
    schedule_list = []

    # Generate schedule based on the duration
    if duration == "once":
        if start_date <= end_date:
            schedule_list.append(start_date)
    else:
        current_date = start_date
        while current_date <= end_date:
            schedule_list.append(current_date)
            if duration in ["daily", "weekly"]:
                current_date += frequency[duration]
            elif duration == "monthly":
                current_date = current_date.replace(
                    month=current_date.month + 1 if current_date.month < 12 else 1,
                    year=current_date.year if current_date.month < 12 else current_date.year + 1
                )
            elif duration == "yearly":
                current_date = current_date.replace(year=current_date.year + 1)

    # Convert datetime objects to strings if necessary
    schedule_list_str = [date.strftime("%Y-%m-%d") for date in schedule_list]
    
    return schedule_list_str


# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            # Creating userprofile entry
            user = get_object_or_404(User, username=form.get_user())
            user_profile, created = UserProfile.objects.update_or_create(user=user,
            defaults={
                'is_content_manager': False,
                'ri_name': "",
                'message': "message",
                'user_name' : "",
            })
            user_profile.save()
            print("Created user profile ... ... ...")

            login(request, form.save())

            
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request): 
    print("You are inside post method ...")
    if request.method == "POST": 
        
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())

            print("User information after logging in", form.get_user())

            user = get_object_or_404(User, username=form.get_user())
            print('Printing user', user)
            user_id = user.id
            if UserProfile.objects.filter(user=user).exists():
                user_profile = UserProfile.objects.get(user=user)
                request.session['user'] = user_profile.user_name
                request.session['RI'] = user_profile.RI_name
                request.session['user_id'] = str(form.get_user())
                request.session['id'] = user.id
                request.session['role'] = user_profile.role
                #request.session['user_profile'] = user_profile

            else:
                user_profile = None  
                request.session['user'] = None
                request.session['RI'] = None
                request.session['user_id'] = None
                request.session['id'] = None
                request.session['role'] = 0
                #request.session['user_profile'] = None
            
            print("Printing the session variables ...", request.session["user"], request.session["RI"])

            return redirect("users:scheduler")
        
            
            # /search/users/test
            #return redirect("posts:list")
    else: 
        form = AuthenticationForm()

    
    return render(request, 'login/login.html', { "form": form })


def logout_view(request):
    logout(request)
    print("you are in logout view")
    
    # Find a way to make this line work: This is more elegent
    #return redirect("opensemanticsearch:search")
    
    return redirect("/search")
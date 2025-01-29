from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login

from django.contrib.auth.models import User
from .models import SchedulerList, UserProfile
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q



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
    

    
    # Run the loop over scheduled list

    return schedule_list_str




"""
request.session['user'] = "Nafis Tanveer Islam"
request.session['RI'] = "SIOS"

"""
def create_schedule(request):
    
    if request.method == "POST": 
        
        print("before validity checking ...")
        duration = request.POST.get('duration')
        indexing_type = request.POST.get('indexing_type')
        operation = request.POST.get('operation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        print(duration, indexing_type, operation, start_date, end_date)
        schedules = generate_schedule_list(duration=duration, start_date_str=start_date, end_date_str=end_date)

        updated_list = []
        for idx, schedule in enumerate(schedules):
            

            # 4 values for the last column: Pending, Indexing, Complete, Failed 
            updated_list.append([request.session['user'], request.session['RI'], "dummy/file/path", indexing_type, operation, schedule, "Pending"])

        print("Printing final schedules created", updated_list)


        for entry in updated_list:
            print("Creating list ... ")
            SchedulerList.objects.create(
                user_name=entry[0],
                RI_name=entry[1],
                file_path=entry[2],
                indexing_type=entry[3],
                operation=entry[4],
                execution_date=timezone.datetime.strptime(entry[5], "%Y-%m-%d"),
                completion=entry[6]
        )
    print('Role of user ...', request.session['role'])
    if request.session['role'] == 2:
        schedules = SchedulerList.objects.all().order_by('execution_date')    
    else:
        schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')
    
    paginator = Paginator(schedules, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #request_user_list = UserProfile.objects.filter(is_RI=False).all()
    request_user_list = UserProfile.objects.filter(is_RI=False, request=True).all()


    user = get_object_or_404(User, id=int(request.session['id']))
    user_profile = UserProfile.objects.filter(user=user).first()  # Returns None if not found
    return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 'id' : request.session['id'], 'user_profile' : user_profile, 'request_user_list' : request_user_list})

    #return render(request, "users/users.html", {'schedules' : schedules})


def edit_schedule(request, schedule_id):

    print("You are inside edit schedule")

    schedule = get_object_or_404(SchedulerList, id=schedule_id)

    schedule.indexing_type = request.POST.get('indexing_type')
    schedule.operation = request.POST.get('operation')
    schedule.execution_date = request.POST.get('execution_date')
    # May need to add logic if date is or is not changed
    schedule.completion = "Pending"

    schedule.save()

    print('Role of user ...', request.session['role'])
    if request.session['role'] == 2:
        schedules = SchedulerList.objects.all().order_by('execution_date')    
    else:
        schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')
    paginator = Paginator(schedules, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    return redirect("users:scheduler")
    #return redirect(request, 'users/users.html', {'page_obj': page_obj})

def delete_schedule(request, schedule_id):

    print("You are inside delete schedule")

    # Write logic to delete the schedule
    schedule = get_object_or_404(SchedulerList, id=schedule_id)
    schedule.delete()

    
    print('Role of user ...', request.session['role'])
    if request.session['role'] == 2:
        schedules = SchedulerList.objects.all().order_by('execution_date')    
    else:
        schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')
    paginator = Paginator(schedules, 7)  # Show 5 schedules per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get schedules for the current page

    return redirect("users:scheduler")
    #return redirect(request, 'users/users.html', {'page_obj': page_obj})


# Create your views here.
def scheduler(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("posts:list")
    else:
        form = UserCreationForm()

    #schedules = get_schedules(request)
    schedules = {}

    print("*** Printing the authentication status ***", request.user.is_authenticated)
    if request.user.is_authenticated:

        #print("Inside scheduler", request.session['user'], request.session['RI'])
        
        print('Role and ID of user ...', request.session['role'], request.session['id'])
        if request.session['role'] == 2:
            schedules = SchedulerList.objects.all().order_by('execution_date')    
        else:
            schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')       
        paginator = Paginator(schedules, 7)  # Show 7 schedules per page

        page_number = request.GET.get('page')  # Get the current page number
        page_obj = paginator.get_page(page_number)  # Get schedules for the current page
        
        

        #request_user_list = UserProfile.objects.filter(is_RI=False).all()
        request_user_list = UserProfile.objects.filter(is_RI=False, request=True).all()
        complete_user_list = UserProfile.objects.filter(Q(role=0) | Q(role=1))


        if UserProfile.objects.filter(user=request.session['id']).exists():
            user = get_object_or_404(User, id=int(request.session['id']))
            user_profile = UserProfile.objects.filter(user=user).first() 
            print("user profile", user_profile)
        else:
            user_profile = None
        return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 
                                                    'id' : request.session['id'], 'user_profile' : user_profile, 
                                                    'request_user_list' : request_user_list, 'complete_user_list' : complete_user_list})

        #return render(request, "users/users.html", {'schedules': schedules})
    return redirect("login:login")



def save_profile(request, id):


    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        
        # Retrieve form data
        is_content_manager = request.POST.get("is_content_manager") == "on"
        print("printing content manger", is_content_manager)
        ri_name = request.POST.get("ri_name") if is_content_manager else ""
        print("printing riname", ri_name)
        message = request.POST.get("message") if is_content_manager else ""
        email = request.POST.get('email')
        name = request.POST.get("user_name")
        req = True if is_content_manager else False
        # Create or update the UserProfile
        user_profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'is_content_manager': is_content_manager,
                'RI_name': ri_name,
                'message': message,
                'email': email,
                'user_name' : name,
                'request' : req
            }
        )   
        user_profile.save()
    

    if request.session['role'] == 2:
        schedules = SchedulerList.objects.all().order_by('execution_date')    
    else:
        schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')       
    paginator = Paginator(schedules, 7)  # Show 7 schedules per page

    #request_user_list = UserProfile.objects.filter(is_RI=False).all()
    request_user_list = UserProfile.objects.filter(is_RI=False, request=True).all()
    complete_user_list = UserProfile.objects.filter(Q(role=0) | Q(role=1))

    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get schedules for the current page
    
    #return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 'id' : request.session['id'], 'user_profile' : user_profile, 'request_user_list' : request_user_list})
    return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 
                                                    'id' : request.session['id'], 'user_profile' : user_profile, 
                                                    'request_user_list' : request_user_list, 'complete_user_list' : complete_user_list})

def request_resolve(request, id):

    print("printing ID and type", id, type(id))
    if request.method == "POST":
        decision = request.POST.get('action')
        user = get_object_or_404(User, username=id)
        print("Printing user", user)
        
        if decision == 'approve':
            user_profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role' : 1,
                    'is_RI' : True
                }
            )   
            user_profile.save()


        

        elif decision == 'deny':
            user_profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role' : 0,
                    'is_RI' : False,
                    'request' : False,
                }
            )   
            user_profile.save()

        elif decision == 'decomission':
            user_profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role' : 0,
                    'is_RI' : False,
                    'request' : False,
                    
                }
            )   
            user_profile.save()
       

    if request.session['role'] == 2:
        schedules = SchedulerList.objects.all().order_by('execution_date')    
    else:
        schedules = SchedulerList.objects.filter(RI_name=request.session['RI']).order_by('execution_date')       
    paginator = Paginator(schedules, 7)  # Show 7 schedules per page

    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get schedules for the current page
    
    

    #request_user_list = UserProfile.objects.filter(is_RI=False).all()
    request_user_list = UserProfile.objects.filter(is_RI=False, request=True).all()
    complete_user_list = UserProfile.objects.filter(Q(role=0) | Q(role=1))
    
    if UserProfile.objects.filter(user=request.session['id']).exists():
        user = get_object_or_404(User, id=int(request.session['id']))
        user_profile = UserProfile.objects.filter(user=user).first() 
    else:
        user_profile = None
    #return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 'id' : request.session['id'], 'user_profile' : user_profile, 'request_user_list' : request_user_list})
    return render(request, 'users/users.html', {'page_obj': page_obj, 'role' : request.session['role'], 
                                                    'id' : request.session['id'], 'user_profile' : user_profile, 
                                                    'request_user_list' : request_user_list, 'complete_user_list' : complete_user_list})
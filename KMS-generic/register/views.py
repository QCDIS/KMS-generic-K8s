from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from users.models import UserProfile
from django.contrib.auth.models import User




# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            print("Validity checking passed of register", request.POST)

            user = get_object_or_404(User, username=request.POST.get('username'))
            user_profile, created = UserProfile.objects.update_or_create(user=user,
            defaults={
                'role' : 0,
                'message': "",
                'user_name' : "",
                'is_RI' : False,
            })
            user_profile.save()

            return redirect('login:login')
            #return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, "register/register.html", { "form": form })


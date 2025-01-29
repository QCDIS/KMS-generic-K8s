from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.





class SchedulerList(models.Model):
    
    RI_name =  models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    indexing_type = models.CharField(max_length=10)
    operation = models.CharField(max_length=10)
    execution_date = models.DateField()
    completion = models.CharField(max_length=20)


    def __str__(self):
        return f"Schedule by {self.RI_name} from {self.user_name} to {self.operation}"
    

class IndexingLog(models.Model):
    RI_name =  models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    ending_time = models.DateTimeField()

    indexing_type = models.CharField(max_length=10)
    operation = models.CharField(max_length=10)

    duration = models.CharField(max_length=40)
    success = models.BooleanField()

    def __str__(self):
        return f"Logging of the user {self.user_name} from  {self.RI_name}, and status is {self.success}"
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.PositiveSmallIntegerField(default=0)
    RI_name = models.CharField(max_length=255)
    message = models.CharField(max_length=2048)
    request = models.BooleanField(default=False)
    is_RI = models.BooleanField(default=False)
    #request_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Profile of the user {self.user_name} from {self.RI_name} with the role {self.role}"
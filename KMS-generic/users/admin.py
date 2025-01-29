from django.contrib import admin
from .models import SchedulerList
from .models import IndexingLog
from .models import UserProfile
# Register your models here.



admin.site.register(SchedulerList)
admin.site.register(IndexingLog)
admin.site.register(UserProfile)
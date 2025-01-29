import os
import django
from datetime import date, datetime
import requests
from django.utils import timezone
from datetime import timedelta



"""
class SchedulerList(models.Model):
    
    RI_name =  models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    indexing_type = models.CharField(max_length=10)
    operation = models.CharField(max_length=10)
    execution_date = models.DateField()
    completion = models.CharField(max_length=20)

"""

"""
http://145.100.135.113/dataset/datasetIndexer/
http://145.100.135.113/webIndexer/  
http://145.100.135.113/api/apiIndexer/
http://145.100.135.113/notebook/notebookIndexer/


"""

api_mapping = {
    'dataset' : 'http://145.100.135.113/dataset/datasetIndexer/',
    'web' : 'http://145.100.135.113/webIndexer/',
    'api' : 'http://145.100.135.113/api/apiIndexer/',
    'notebook' : 'http://145.100.135.113/notebook/notebookIndexer/'
}

# Set up Django settings environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opensemanticsearch.settings')
django.setup()

# Import models after setup
from users.models import SchedulerList
from users.models import IndexingLog

def is_time_1159pm():
    # Get the current system time
    current_time = datetime.now().time()
    #print("printing current time ", current_time)
    
    # Check if it's 11:59 PM
    return current_time.hour == 23 and current_time.minute == 59

def get_todays_schedules():
    today = date.today()
    schedules_today = SchedulerList.objects.filter(execution_date=today)

    indexing_log = IndexingLog.objects.all()
    # for log in indexing_log:
    #     print(log)


    while True:
        if is_time_1159pm():
            print("Correct time ...")
            final_daily_list = []
            url = ""
            for schedule in schedules_today:
                if schedule.indexing_type == "Web":
                    final_daily_list.append(api_mapping['web'])
                    url = api_mapping['web']
                elif schedule.indexing_type == "Dataset":
                    final_daily_list.append(api_mapping['dataset'])
                    url = api_mapping['dataset']
                elif schedule.indexing_type == "API":
                    final_daily_list.append(api_mapping['api'])
                    url = api_mapping['api']
                elif schedule.indexing_type == "Notebook":
                    final_daily_list.append(api_mapping['notebook'])
                    url = api_mapping['notebook']

                if schedule.operation == 'Create':
                    final_daily_list[-1] += '/create'
                    url += '/create'
                else:
                    final_daily_list[-1] += '/delete' 
                    url += '/delete'
                #print('Schedule Elements ...', schedule.RI_name, schedule.user_name, schedule.file_path, schedule.indexing_type, schedule.operation, schedule.completion)
                
                ### DETERMINE THE SCHEMA FOR THE NEW TABLE ###
                start_time = timezone.now()
                # Create the API list to call
                response = requests.get(url)
                schedule.completion = "Pending"
                schedule.save()


                
                
                
                if response.status_code == 200:
                    schedule.completion = "Success"
                    schedule.save()
                    # posts = response.json()
                    # return posts
                else:
                    schedule.completion = "Fail"
                    schedule.save()
                    # Fail Code in SchewdulerList 
                    pass
                
                # Update the log file

                success = True if schedule.completion == "Success" else False
                ending_time = timezone.now()
                log_entry = IndexingLog(
                    RI_name=schedule.RI_name,
                    user_name=schedule.user_name,
                    start_time=start_time,
                    ending_time=ending_time, 
                    indexing_type=schedule.indexing_type,
                    operation=schedule.operation,
                    duration=ending_time - start_time,
                    success=success
                )
                
                log_entry.save()
                
                #print(f"Schedule for {schedule.user_name} on {schedule.execution_date}")

            print(final_daily_list)


            # Update the SchedulerList database "Pending"
            # Update the Log Table with starting time () 
            # Call the API
            # When done, update the SchedulerList database to "Finished/Failed"
            # Update the log
    

# Call the function
if __name__ == "__main__":
    get_todays_schedules()

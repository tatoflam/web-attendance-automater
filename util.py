from datetime import datetime
import jpholiday
import yaml

# Check if the date (datetime object) is a business day (weekday and 
# not a holiday) in Japan
# date: datetime object
def isBusinessDay(date):
    # Date = datetime(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if date.weekday() >= 5 or jpholiday.is_holiday(date):
        print('%s is not a business day in Japan' % date)
        return False
    else:
        print('%s is a business day in Japan' % date)
        return True

# Check if the date is in a vacation list in vacation.yaml
# In vacation yaml, you can list dates of a vacation
# Example of vacation.yaml
# vacation:
# - 2022-12-28
# - 2022-12-29
# - 2022-12-30
# date: datetime object
def isVacation(date):
    vacation = False
    
    # Open the YAML file and read the data
    with open('vacation.yaml', 'r') as f:
        data = yaml.safe_load(f)

    # print(data)
    # Create a list of datetime objects from the data
    # datetime_list = [datetime.fromisoformat(d) for d in data['vacation']]
    datetime_list = [d for d in data['vacation']]
    if date in datetime_list:
        vacation = True
    else:
        vacation = False
    return vacation
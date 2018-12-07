from datetime import timedelta,datetime,date

def daysrange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
def weeksrange(start_date, end_date,jour):
        first_date=start_date + timedelta(jour-start_date.isoweekday())
        for n in range(int (end_date.isocalendar()[1] - start_date.isocalendar()[1])):
                yield first_date + timedelta(weeks=n)
def monthsrange(start_date, end_date,day_of_month):
        first_date=start_date + timedelta(day_of_month - start_date.day)
        for n in range(end_date.month - start_date.month + 1) :
                yield first_date.replace(month=start_date.month + n)

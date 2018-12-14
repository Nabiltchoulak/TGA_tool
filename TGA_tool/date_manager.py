from datetime import timedelta,datetime,date

def daysrange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
def weeksperiod(start_date, end_date,jour):
        diff_first_date=jour-start_date.isoweekday()
        if diff_first_date > 0:
                first_date=start_date + timedelta(diff_first_date)
        else : 
                 first_date=start_date + timedelta(7+diff_first_date)
        for n in range((end_date.toordinal()-start_date.toordinal())//7):
                yield first_date + timedelta(weeks=n)
def monthsperiod(start_date, end_date,day_of_month):#put an limit  of 5 years later
        first_date=start_date + timedelta(day_of_month - start_date.day) 
        periode=(end_date.toordinal()-start_date.toordinal())
        if periode==59 or periode==58 :#when we have january + february 58/59 days so intervall//30==1
                periode+=2
        for n in range(periode//30) :
                mth=(start_date.month + n)
                if mth > 12 :
                        mth=mth%12#Eviter le cas qu'un mois dépasse 12
                        first_date.replace(year=first_date.year+1)
                yield first_date.replace(month=(mth))
def spe_daysperiod(start_date, end_date,period):
        sweeping_date=start_date
        while sweeping_date <= end_date :
                yield sweeping_date 
                sweeping_date+=timedelta(period)
def spe_weeksperiod(start_date, end_date,period):
        sweeping_date=start_date
        while sweeping_date <= end_date :
                yield sweeping_date 
                sweeping_date+=timedelta(weeks=period)
def spe_monthsperiod(start_date, end_date,period,day_of_month):
        first_date=start_date + timedelta(day_of_month - start_date.day)
        month_interval=(end_date.toordinal()-start_date.toordinal())//30
        for n in range(month_interval//period) :
                
                mth=(start_date.month + period*n)
                if mth > 12 :
                        mth=mth%12#Eviter le cas qu'un mois dépasse 12
                        first_date.replace(year=first_date.year+1)
                yield first_date.replace(month=(mth))
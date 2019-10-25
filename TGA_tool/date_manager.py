from datetime import timedelta,datetime,date

def daysrange(start_date, end_date):#Chaque jour 
    for n in range(int ((end_date - start_date).days)+1):
        date= start_date + timedelta(n)
        if date.isoweekday()==1 or date.isoweekday()==7 :
                    pass
        else :
                yield date 

def daysrange_summer_camp(start_date):#Chaque jour
        end_date=start_date+ timedelta(7)
        for n in range(int ((end_date - start_date).days)+1):
                date= start_date + timedelta(n)
                if date.isoweekday()==5 or date.isoweekday()==6 :
                        pass
                else :
                        yield date 



def weeksperiod(start_date, end_date,jour):#Chaque semaine
        diff_first_date=jour-start_date.isoweekday()
        if diff_first_date > 0:
                first_date=start_date + timedelta(diff_first_date)
        else : 
                 first_date=start_date + timedelta(7+diff_first_date)
        for n in range((end_date.toordinal()-start_date.toordinal())//7 + 1):
                yield first_date + timedelta(weeks=n)

def two_times_weeks_period(start_date, end_date,jour, jour_two):#2 fois par semaine
        diff_first_date=jour-start_date.isoweekday()
        diff_second_date=jour_two-start_date.isoweekday()

        first_date = start_date + timedelta(diff_first_date) if diff_first_date > 0 else start_date + timedelta(7+diff_first_date)
        second_date = start_date + timedelta(diff_second_date) if diff_second_date > 0 else start_date + timedelta(7+diff_second_date)

        
        for n in range((end_date.toordinal()-start_date.toordinal())//7 +1):
                yield first_date + timedelta(weeks=n)
                yield second_date + timedelta(weeks=n)

def three_times_weeks_period(start_date, end_date,jour, jour_two,jour_three):#2 fois par semaine
        diff_date=[]
        first_dates=[]
        for day in [jour,jour_two,jour_three]:
                diff_date.append(day-start_date.isoweekday())
        
        for diff in diff_date:
                if diff > 0 :
                        first_dates.append(start_date + timedelta(diff))  
                else : 
                        first_dates.append(start_date + timedelta(7+diff) )
        

        
        for n in range((end_date.toordinal()-start_date.toordinal())//7 + 1):
                for date in first_dates :
                        yield date + timedelta(weeks=n)
               







def monthsperiod(start_date, end_date,day_of_month):#put an limit  of 5 years later ####Chaque mois
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




def spe_daysperiod(start_date, end_date,period):#Chaque x jours
        sweeping_date=start_date
        while sweeping_date <= end_date :
                yield sweeping_date 
                sweeping_date+=timedelta(period)




def spe_weeksperiod(start_date, end_date,period):#Chaque X semaines 
        sweeping_date=start_date
        while sweeping_date <= end_date :
                yield sweeping_date 
                sweeping_date+=timedelta(weeks=period)



def spe_monthsperiod(start_date, end_date,period,day_of_month):#Chaque x mois 
        first_date=start_date + timedelta(day_of_month - start_date.day)
        month_interval=(end_date.toordinal()-start_date.toordinal())//30
        for n in range(month_interval//period) :
                
                mth=(start_date.month + period*n)
                if mth > 12 :
                        mth=mth%12#Eviter le cas qu'un mois dépasse 12
                        first_date.replace(year=first_date.year+1)
                yield first_date.replace(month=(mth))

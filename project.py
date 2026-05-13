from rich import print
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import sleep
import re
print(Panel("[bold]The Tail End", subtitle='subtitle'))
def calculate_remaining(dictn, age):
    personalfreq=[]
    for event,times in dictn.items():
        used=times*age
        total=times*80
        personalfreq.append({'event': event, 'used': used, 'total': total})
    return personalfreq
def parse_frequency(s):
    year_freq=re.search(r'([0-9]+) times? a (day|week|month|year)',s)
    if year_freq:
        times=int(year_freq.group(1))
        timespan=year_freq.group(2)
        return times, timespan
    else:
        raise ValueError
def calculate_life_stats(dob, life_expectancy=80):
    death=dob+relativedelta(years=life_expectancy)
    age_years=relativedelta(date.today(),dob).years
    years_remaining=relativedelta(death,date.today()).years
    percent_elapsed=(age_years*100)/life_expectancy
    return {'age':age_years,'timeelapsed':years_remaining,'percent':percent_elapsed}
def main():
    name=input('Enter your first name: ').strip().lower().capitalize()
    while True:
        try:
            dob_str=input('Enter your date of birth in YYYY-MM-DD format: ')
            dob=datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            continue
        else:
            break
    stats=calculate_life_stats(dob)
    print('Your life, in weeks')
    with Progress() as progress:
        task_id=progress.add_task('Years elapsed', total=80)
        for _ in range(0,(stats['age'])):
                sleep(0.02)
                progress.update(task_id, advance=1)
    per_line = 30
    count = 0

    for i in range(round(stats['age'] * 52.143)):
        print('▣', end=' ')
        count += 1

        if count % per_line == 0:
            print()

    for i in range(round((stats['timeelapsed'] + 1) * 52.143)):
        print('□', end=' ')
        count += 1

        if count % per_line == 0:
            print()
    print()
    print(f'{name}, you have used {stats['percent']}% or {round(stats['age']*52.143)} weeks of your life. You have only ~{round(stats['timeelapsed']*52.143)} weeks remaining')
    print("What's elapsed?")
    rates = {
    "Heartbeats": 36800000,
    "Sunrises": 365.25,       
    "Full Moons": 12.37,        
    "Birthdays": 1,
    "Summers": 1,
    "Leap Years": 0.25,          
    "Lunar Eclipses": 2.28,
    "World Cups and Olympics": 0.25
    }
    age = stats['age']
    expectancy = 80

    results = {}

    for event, rate in rates.items():
        total = (rate * expectancy)
        used = (rate * age)
        remaining = total - used
        percentage = (used/total) * 100 if total > 0 else 0
        
        results[event] = {
            "used": int(used),
            "total": int(total),
            "remaining": int(remaining),
            "percentage": round(percentage)
        }
    for event, data in results.items():
        print(f'You have experienced {data['used']}/{data['total']} {event}')
        print(f"{event} remaining: {data['remaining']}")
    print('Your turn!')
    print('You can enter upto 5 activities you love doing: ')
    activities={}
    for i in range(0,5):
        activity=input("What's something you love doing(an activity)?")
        try:
            frequencyunit=input('How many times do you do this?(x time(s) a day/week/month/year), type exit to stop asking this')
            if frequencyunit.strip().lower()=='exit':
                break
            times, timespan=parse_frequency(frequencyunit)
        except ValueError:
            continue
        if timespan=='day':
            times=round(times*365.125)
        elif timespan=='week':
            times=round(times*52.1429)
        elif timespan=='month':
            times=times*12
        else:
            pass
        activities[activity]=times
    remainingstats=calculate_remaining(activities, (stats['age']))
    for i in remainingstats:
        print(f'You have experienced {i['used']}/{i['total']} of "{i['event']}"')
        print(f'"{i['event']}" remaining: {(i['total']-i['used'])}')
if __name__=='__main__':
    main()
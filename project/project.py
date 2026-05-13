from rich import print
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import sleep
print(Panel("[bold]The Tail End", subtitle='subtitle'))
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
    for i in range(0,round(stats['age']*52.143)):
        print('▣', end=' ')
        sleep(0.00001)
    for i in range(0,round((stats['timeelapsed']+1)*52.143)):
        print('□', end=' ')
        sleep(0.0000001)
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
        total = rate * expectancy
        used = rate * age
        remaining = total - used
        percentage = (used / total) * 100 if total > 0 else 0
        
        results[event] = {
            "used": int(used),
            "total": int(total),
            "remaining": int(remaining),
            "percentage": round(percentage)
        }
    for event, data in results.items():
         with Progress() as progress:
            task_id=progress.add_task(f'{event} elapsed', total=100)
            for _ in range(0,data['percentage']):
                sleep(0.02)
                progress.update(task_id, advance=1)
                print(f"{event} remaining: {data['remaining']}")
if __name__=='__main__':
    main()
from rich import print
from rich.panel import Panel
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import sleep
import re
from rich.progress import Progress

CHILDHOOD_END_AGE = 18
COHAB_DAYS_PER_YEAR = 350

def parse_frequency(s):
    s = s.strip().lower()
    s = (s.replace("once", "1 times")
          .replace("twice", "2 times")
          .replace("thrice", "3 times"))

    m = re.search(
        r"([0-9]+)\s*(?:times?\s*)?(?:a\s+|per\s+)?(day|week|month|year)",
        s,
    )
    if m:
        return int(m.group(1)), m.group(2)

    m = re.search(r"([0-9]+)\s*times?\s+(daily|weekly|monthly|yearly|annually)", s)
    if m:
        span = {"daily":"day","weekly":"week","monthly":"month",
                "yearly":"year","annually":"year"}[m.group(2)]
        return int(m.group(1)), span

    for word, span in [("daily","day"),("weekly","week"),
                       ("monthly","month"),("yearly","year"),("annually","year")]:
        if word in s:
            return 1, span

    for span in ("day","week","month","year"):
        if f"every {span}" in s:
            return 1, span

    raise ValueError


def to_per_year(times, span):
    if span == "day":
        return round(times * 365.25)
    if span == "week":
        return round(times * 52.1429)
    if span == "month":
        return times * 12
    return times


def parse_relation(s):
    s = s.strip().lower()
    for term in [
        "grandmother","grandfather","grandma","grandpa","grandparent",
        "nana","nani","dadi","ammachi",
    ]:
        if term in s:
            return "grandparent"
    for term in [
        "mother","father","mom","mum","dad","papa","mama",
        "amma","appa","achan","parent",
    ]:
        if term in s:
            return "parent"
    for term in ["brother", "sister", "sibling", "sis", "bro"]:
        if term in s:
            return "sibling"
    for term in ["partner", "spouse", "husband", "wife", "boyfriend", "girlfriend"]:
        if term in s:
            return "partner"
    for term in ["son", "daughter", "child", "kid"]:
        if term in s:
            return "child"
    if "friend" in s:
        return "friend"
    return None


def calculate_life_stats(dob, life_expectancy=80):
    death = dob + relativedelta(years=life_expectancy)
    age_years = relativedelta(date.today(), dob).years
    years_remaining = max(0, relativedelta(death, date.today()).years)
    percent_elapsed = (age_years * 100) / life_expectancy
    return {"age": age_years, "timeleft": years_remaining, "percent": percent_elapsed}


def calculate_remaining(dictn, age, life_expectancy=80):
    personalfreq = []
    for event, times in dictn.items():
        used = times * age
        total = times * life_expectancy
        personalfreq.append(
            {"event": event, "used": used, "total": total, "remaining": total - used}
        )
    return personalfreq


def calculate_relation(peopledict, age, timeleft, life_expectancy=80):
    relationstats = {}
    for person, values in peopledict.items():
        times = max(0, values["times"])
        their_age = max(0, min(values["age"], life_expectancy))
        relation = values["relation"]
        years_left_together = max(0, min(timeleft, life_expectancy - their_age))

        if relation == "sibling":
            relationship_years_so_far = min(age, their_age)
            older_age = max(age, their_age)
            years_since_older_left = max(0, older_age - CHILDHOOD_END_AGE)
            cohabitation_years_so_far = max(
                0, relationship_years_so_far - years_since_older_left
            )
            apart_years_so_far = relationship_years_so_far - cohabitation_years_so_far
            meetings_so_far = (
                cohabitation_years_so_far * COHAB_DAYS_PER_YEAR
                + apart_years_so_far * times
            )
            future_cohabitation_years = max(
                0, min(years_left_together, CHILDHOOD_END_AGE - older_age)
            )
            future_apart_years = max(0, years_left_together - future_cohabitation_years)
            remaining_meetings = (
                future_cohabitation_years * COHAB_DAYS_PER_YEAR
                + future_apart_years * times
            )

        elif relation == "parent":
            childhood_years_so_far = min(age, CHILDHOOD_END_AGE)
            adult_years_so_far = max(0, age - CHILDHOOD_END_AGE)
            meetings_so_far = (
                childhood_years_so_far * COHAB_DAYS_PER_YEAR
                + adult_years_so_far * times
            )
            future_childhood_years = max(
                0, min(CHILDHOOD_END_AGE - age, years_left_together)
            )
            future_adult_years = max(0, years_left_together - future_childhood_years)
            remaining_meetings = (
                future_childhood_years * COHAB_DAYS_PER_YEAR
                + future_adult_years * times
            )

        elif relation == "child":
            cohab_so_far = min(their_age, CHILDHOOD_END_AGE)
            adult_so_far = max(0, their_age - CHILDHOOD_END_AGE)
            meetings_so_far = cohab_so_far * COHAB_DAYS_PER_YEAR + adult_so_far * times
            future_cohab = max(
                0, min(CHILDHOOD_END_AGE - their_age, years_left_together)
            )
            future_adult = max(0, years_left_together - future_cohab)
            remaining_meetings = (
                future_cohab * COHAB_DAYS_PER_YEAR + future_adult * times
            )

        else:
            years_known = values.get("years_known", max(0, age - CHILDHOOD_END_AGE))
            meetings_so_far = years_known * times
            remaining_meetings = years_left_together * times

        total_meetings = meetings_so_far + remaining_meetings
        percent_used = (
            (meetings_so_far / total_meetings * 100) if total_meetings > 0 else 0
        )
        relationstats[person] = {
            "relation": relation,
            "meetings_so_far": int(meetings_so_far),
            "remaining_meetings": int(remaining_meetings),
            "total_meetings": int(total_meetings),
            "percent_used": round(percent_used),
        }
    return relationstats


def pause():
    print("[dim](press enter)[/dim] ", end="")
    input()


def main():
    print(Panel("[bold]The Tail End", subtitle="after Tim Urban"))
    print()
    print("It is easy to imagine more time than you have.")
    print("This is a look at what is actually left.\n")
    sleep(0.8)

    name = input("First, your name please: ").strip().lower().capitalize()

    while True:
        try:
            dob_str = input("And the day you were born (YYYY-MM-DD): ").strip()
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob > date.today():
                print("That is in the future. Try again.")
                continue
            if (date.today() - dob).days > 365.25 * 120:
                print("That is too long ago. Try again.")
                continue
            break
        except ValueError:
            print("Could not read that. Use YYYY-MM-DD.")

    le_str = input("Life expectancy to use (enter for 80): ").strip()
    try:
        life_expectancy = int(le_str) if le_str else 80
    except ValueError:
        life_expectancy = 80

    stats = calculate_life_stats(dob, life_expectancy)
    age = stats["age"]

    if age >= life_expectancy:
        print(f"\n{name}, you have already outlived the {life_expectancy}-year mark.")
        print("The math here does not apply to you. Live well.\n")
        return

    print(f"\n{name}, here are the weeks of your life.\n")
    sleep(1.2)

    per_line = 52
    count = 0
    weeks_lived = round(age * 52.143)
    weeks_left = round(stats["timeleft"] * 52.143)
    for _ in range(weeks_lived):
        print("▣", end="")
        count += 1
        if count % per_line == 0:
            print()
    for _ in range(weeks_left):
        print("□", end="")
        count += 1
        if count % per_line == 0:
            print()
    print("\n")
    sleep(1)
    print(f"~{weeks_left:,} weeks left.")
    print(
        f'You have used {int(stats["percent"])}% of an {life_expectancy}-year life.\n'
    )
    pause()

    print(f"\nA few things you will still see, {name}:\n")
    sleep(0.4)
    rates = {
        "Sunrises🌅": 365.25,
        "Mondays🌚": 52.143,
        "Full moons🌕": 12.37,
        "Summers🌞": 1,
        "Birthdays🎂": 1,
        "Olympic Games and World Cups⚽️": 0.25,
    }
    for event, rate in rates.items():
        remaining = round(rate * stats["timeleft"])
        print(
            f'You have experienced {round(rate*stats["age"])}/{round(rate*life_expectancy)} {event}'
        )
        print(f"  {event} left: {remaining:,}")
        sleep(0.2)
    print()
    pause()

    print("\nNow your turn! Let's try this with the things you do")
    print("A morning coffee. The Sunday paper. A walk you take. A sport you watch\n")
    activities = {}
    while True:
        activity = input("Something you love to do (enter to move on): ").strip()
        if not activity:
            break
        try:
            freq = input(
                'How often? (e.g. "twice a week", "every day", "once a year"): '
            )
            times, span = parse_frequency(freq)
        except ValueError:
            print("Could not read that. Skipping.\n")
            continue
        activities[activity] = to_per_year(times, span)

    if activities:
        print()
        for activity, times_per_year in activities.items():
            remaining = times_per_year * stats["timeleft"]
            print(
                f'You have experienced {times_per_year*stats["age"]}/{times_per_year*life_expectancy} "{activity}"'
            )
            print(f"{activity}: about {remaining:,} more, at {times_per_year} a year.")
        print()
        pause()

    print("\nMost of those happen at a roughly even rate every year of your life,")
    print(
        "which means you have used about as much of them as you have used of your time."
    )
    sleep(0.5)
    pause()
    print("\nThe next part is different.\n")
    sleep(0.6)
    print("Time with the people you love is not spread evenly.")
    print(
        "It is front-loaded, into childhood, into the years you lived in the same house."
    )
    print("What is left, for most relationships, is a surprisingly small number.\n")
    pause()
    print("\n[bold]Relationships[/bold]\n")
    sleep(0.3)

    people = {}
    while True:
        person = input("Who is a person you love? (enter to stop): ").strip()
        if not person:
            break
        rel = parse_relation(
            input(
                f"Who is {person} to you? (parent / sibling / grandparent / partner / child / friend): "
            )
        )
        if not rel:
            print("Could not read that. Try one of those words.\n")
            continue
        try:
            their_age = int(input(f"How old is {person}? (type a number): "))
        except ValueError:
            print("Skipping.\n")
            continue
        if their_age < 0 or their_age >= life_expectancy:
            print(
                f"{person} is outside the {life_expectancy}-year model. Using boundary values."
            )
            their_age = max(0, min(their_age, life_expectancy - 1))

        same_city = input(
            f"Do you live in the same city as {person}? (y/n): "
        ).strip().lower().startswith("y")

        will_separate = same_city and (age < 18 or their_age < 18)

        if will_separate:
            print(
                f"You currently live in the same city as {person}. "
                "The math after one of you moves out is what matters here."
            )
            future_same_city = input(
                f"Do you expect to live in the same city as {person} once you/they are adults? (y/n): "
            ).strip().lower().startswith("y")
            default_times = 100 if future_same_city else 10
            ask = f"How often do you think you will see {person} once you live apart?"
        else:
            default_times = 100 if same_city else 8
            ask = f"How often do you usually see {person}?"
        freq = input(f"{ask} (enter for default — about {default_times} a year): ").strip()
        if freq:
            try:
                t, span = parse_frequency(freq)
                times = to_per_year(t, span)
            except ValueError:
                times = default_times
        else:
            times = default_times

        years_known = None
        if rel in ("partner", "friend", "grandparent"):
            default_known = age if rel == "grandparent" else max(0, age - CHILDHOOD_END_AGE)
            raw = input(
                f"How many years have you known {person}? "
                f"(enter for default — {default_known}): "
            ).strip()
            try:
                years_known = int(raw) if raw else default_known
            except ValueError:
                years_known = default_known

        entry = {"times": times, "relation": rel, "age": their_age}
        if years_known is not None:
            entry["years_known"] = years_known
        people[person] = entry

        result = calculate_relation(
            {person: entry}, age, stats["timeleft"], life_expectancy
        )[person]
        print()
        with Progress() as progress:
            task_id = progress.add_task(f"Time spent with {person}", total=100)
            current_progress = 0
            while current_progress < result["percent_used"]:
                sleep(0.05)
                progress.update(task_id, advance=1)
                current_progress += 1
        print(
            f'You have hung out {result["meetings_so_far"]}/{result["total_meetings"]} with "{person}"'
        )
        print(
            f'[bold]You have already spent {result["percent_used"]}% of your time with {person}.[/bold]'
        )
        print(f'About {result["remaining_meetings"]:,} meetings remain.\n')
        sleep(0.6)
        pause()

    if people:
        all_results = calculate_relation(
            people, age, stats["timeleft"], life_expectancy
        )
        ranked = sorted(all_results.items(), key=lambda x: -x[1]["percent_used"])
        top_name, top_data = ranked[0]
        print(
            f"\n{name} — of everyone you named, your time with {top_name} is the most spent."
        )
        print(
            f'{top_data["percent_used"]}% gone. About {top_data["remaining_meetings"]:,} meetings left.'
        )
        pause()

    print("\nThree things worth holding on to:\n")
    print(
        "1) Where you live matters. Time with people in your city is roughly ten times the time with people somewhere else."
    )
    print(
        "2) Priorities matter. Make sure the list is yours, set on purpose, not by inertia."
    )
    print(
        "3) Quality matters. If you are in your last 10% with someone, treat that time as what it is — precious.\n"
    )
    sleep(1.2)
    with Progress() as progress:
        task_id = progress.add_task("% of life used", total=100)
        current_progress = 0
        while current_progress < int(stats["percent"]):
            sleep(0.05)
            progress.update(task_id, advance=1)
            current_progress += 1
    print(
        f'You have used {int(stats["percent"])}% of an {life_expectancy}-year life.\n'
    )
    print("The question is — what will you do with the rest of it?")
    print(f"That is all, {name}. Adios amigo!\n")


if __name__ == "__main__":
    main()

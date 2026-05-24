# The Tail End

#### Video Demo: https://www.youtube.com/watch?v=0STEkAimUSc

#### Description:

A beautiful CLI tool that runs in your terminal that brings your life into perspective, quantifies the moments you have left with your loved ones and the things you love to do finitely-inspired by the works of Tim Urban at Wait But Why-Your life in weeks and The Tail End. A reminder that you so much less time than you think you do. Especially with relationships, most of your time with parents or siblings is front-loaded into childhood. For example, I'm only 15 and yet I've spent 89% of my total time with my sister. The purpose of the project is to help the user realise the finiteness of their existence quantifiably and act on it with morbid statistics.

### Installation and How to Use

Pick the method that works for you. Option 3 requires no installation at all.

---

#### Option 1: Mac

1. Open **Terminal** (press `Command + Space`, type `Terminal`, hit Enter)
2. Run these commands one at a time:

```bash
mkdir tailend
cd tailend
```

3. Create the file and paste the code into it:

```bash
nano project.py
```

Paste the code with `Command + V`, then press `Control + X`, then `Y`, then `Enter` to save.

4. Install the required libraries:

```bash
pip3 install rich python-dateutil
```

5. Run the program:

```bash
python3 project.py
```

---

#### Option 2: Windows

1. Press `Windows + R`, type `cmd`, and hit Enter to open **Command Prompt**
2. Run these commands one at a time:

```cmd
mkdir tailend
cd tailend
```

3. Create the file:

```cmd
notepad project.py
```

A window will open. Paste the code in, save, and close Notepad.

4. Install the required libraries:

```cmd
pip install rich python-dateutil
```

5. Run the program:

```cmd
python project.py
```

> If you get an error saying `python` is not recognized, try `py project.py` instead.

---

#### Option 3: No Installation (Browser-Based via Replit)

This works on any device with a browser. No downloads required.

1. Go to [replit.com](https://replit.com) and create a free account
2. Click **Create Repl**, select **Python** as the template, and give it any name
3. Delete the default code in the editor and paste in the project code
4. Click the **Shell** tab at the bottom and run:

```bash
pip install rich python-dateutil
```

5. Click the green **Run** button at the top

Enjoy!

### Tech Stack

Purely python! runs in your terminal

#### Features

Input age, activities you like to do, and people you love get back the finite number of moments you have left with them/it

#### Program Flow:

The user is asked for their name, date of birth and is confronted with a grid with all the weeks of their expected lives, with the exhausted weeks filled. The number of events like summers, Mondays, world cups they have left is presented to them computed with their age and life expectancy. The user is later prompted to input activities of their own so they can transfer that realization into their own life. The core of the program comes next estimating the amount of meetings they have left with their loved ones accounting for living in the same city, relation and ages. The program ends with a reminder of the person you have the least time left with and a few recommendations.

The entirety of the logic is contained in the project.py file, while the test_project.py file conducts unit tests, the current file README.md provides a description and requirements.txt outline the to-be-installed requirements

#### Build Status and Planned Improvements

Definitely not stopping at this, this is the first prototype. Possible improvements could be adding ascii art, pauses, animations and porting it to the web to make it accessible to people unfamiliar with terminal.

#### Assumptions Made

- Assumed moving out of house by 18
- Assumed death at life expectancy (default 80)
- Assumed 350 days spent together a year when co-habiting
- Assumed 10x increase in meetings when living in same city (source: The Tail End by Tim Urban)
- Assumed being together 8 days a year when living apart

#### Design Choices Made

- using time.sleep and dimmed out enter text to continue to reinforce the message and give the user time and space to soak in the message
- not making it super beautiful at the moment with ascii art etc, currently using rich for formatting
- accepting a wide range of user input including local names like nana, didi, etc (northern belt of india) for grandmother, sister and amma, etc (dravidian belt) for relation apart from the regular anglical relation names.

#### License

MIT © Aditya Suhas Nair

#### Credits

Tim Urban for inspiration - waitbutwhy.com
David Malan and the CS50 team
Neal.fun for immersion mechanics

#### Requirements

- rich
- python-dateutil
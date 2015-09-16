# TIME TRACKER FILLING TOOL

| Author | Email |
| --- | --- |
| Dmytro Soloviov | [dsoloviov@frov.jcu.cz](dsoloviov@frov.jcu.cz) |

TTFT (Time tracker filling tool) is a tool for automated filling the time tracking sheets of ICS FFPW USB (Institute of Complex Systems, Faculty of Fisheries and Protection of Waters, University of South Bohemia). Tool is based on Selenium WebDriver and written in [Python](https://www.python.org/).

### Project structure

```
/src
   __init__.py
   autofill.py
   main.py
   parser.py
dochazka.py
requirements.txt
schedule.txt
config.ini
```

__dochazka.py__ is entry point.

### Dependencies

TTFT relies on [Selenium WebDriver](http://www.seleniumhq.org/). The easiest way to install it is running the PIP utility in root directory of the tool:

```
pip install -r requirements.txt
```

### Configuration file

Configuration file (__config.ini__) contains username and password needed to loging to the tracking system. The valid file structure is following:

```
[Credentials]
Username = your_username
Password = your_password
```

### Creating schedules

TTFT processes special scenario TXT file (__schedule.txt__) and perform command(s) inside it. The command structure is:

```
FILL activity_type FROM start_date TO end_date (start_time:end_time) IN month MONTH
```

Uppercase words are used parsing the command, do not change them. User have to specify activity type (work, vacation, sick leave, etc.), date range (e.g. from 1st to 15th), time on work, month.

Schedule can contain several lines of commands that will be executed one by one:

- work from 1st to 10th
- vacation from 11th to 20th
- work again from 21th to end of the month.

#### Activity types

- 'work'
- 'vacation'
- 'trip' (for business trip)
- 'sick' (for sick leave)

#### Start / end date:

- number (1 to last day of month, e.g. 31)
- 'yesterday'
- 'today'
- 'toworrow'
- 'last' - last day of month
- 'first' - first day of month

#### Start / end time:

The format of time is HH:MM-HH:MM. For example, (07:00-18:00) means working from 7AM to 6PM. Hours can be in range from 00 to 23, minutes - from 00 to 50 (with step 10).

#### Month:

Month can be specified as number (1 for January, 12 for December) or using the word: January, June, etc. Also user can use keyword 'current' to use current month.

#### Schedule examples:

Work from 7AM to 11AM each day from 1st to 10th of October:

```
FILL work FROM 1 TO 10 (07:00-11:00) IN 10 MONTH
```
```
FILL work FROM 1 TO 10 (07:00-11:00) IN October MONTH
```

Vacation from 1st of September (provided it's current month) till today:

```
FILL vacation FROM first TO today (07:00-11:00) IN current MONTH
```
```
FILL vacation FROM 1 TO today (07:00-11:00) IN September MONTH
```
```
FILL vacation FROM 1 TO today (07:00-11:00) IN 9 MONTH
```

__Please keep in mind__ that 'today' keyword means not today's exact date (let's say '3rd of November 2015') but today's day number (3rd day of the month). Therefore using 'today' for following months is legal:

```
FILL work FROM 1 TO today (07:00-11:00) IN current MONTH
```
```
FILL work FROM 1 TO today (07:00-11:00) IN December MONTH
```

__Also__ be sure not to abuse 'first' and 'last' keywords. For example, the following example will cause crash:

```
FILL work FROM last TO first (07:00-11:00) IN December MONTH
```
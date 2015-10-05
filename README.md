# TIME TRACKER FILLING TOOL

| Author | Email |
| --- | --- |
| Dmytro Soloviov | [dsoloviov@frov.jcu.cz](dsoloviov@frov.jcu.cz) |

TTFT (Time tracker filling tool) is a tool for automated filling the time tracking sheets of ICS FFPW USB (Institute of Complex Systems, Faculty of Fisheries and Protection of Waters, University of South Bohemia). Tool is based on [Selenium WebDriver](http://www.seleniumhq.org/) and written in [Python](https://www.python.org/).

### Running

Tool can be started without argument (if __schedule.txt__ is available in tool's root directory):

```
python dochazka.py
```

Also it is possible to provide custom schedule file and/or custom config file:

```
python dochazka.py -f %absolute_path_to_schedule_file%
python dochazka.py -c %absolute_path_to_config_file%
python dochazka.py -c %path_1% -f %path_2%
```

Please make sure that appropriate username and password are provided in __config.ini__.

### Project structure

```
/src
   __init__.py
   autofill.py
   parser.py
dochazka.py
schedule.txt
config.ini
```

### Dependencies

TTFT relies on [Selenium WebDriver](http://www.seleniumhq.org/). The easiest way to install it is via the PIP utility :

```
pip install selenium
```

Also [Firefox](https://www.mozilla.org/en-US/firefox/new/) browser should be installed.

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
FILL activity_type FROM start_date TO end_date (start_time:end_time)
IN month MONTH WITH 'comment_text' COMMENT
```

__All command from FILL to COMMENT is one line__. Uppercase words are used parsing the command, do not change them. User have to specify activity type (work, vacation, sick leave, etc.), date range (e.g. from 1st to 15th), time on work, month.

Schedule can contain several lines of commands that will be executed one by one:

- vacation from 11th to 20th
- sick leave from 21th to end of the month

The following translates into schedule command as:

```
FILL vacation FROM 11 TO 20 (07:00-15:30) IN October MONTH WITH 'vacation' COMMENT
FILL sick FROM 21 TO last (07:00-15:30) IN October MONTH WITH 'sick leave' COMMENT
```

#### Activity types

- 'vacation': Dovolená
- 'trip': Služebni cesta
- 'sick': Nemoc

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

#### Comment:

Comment is a text wrapped in ''.

#### Schedule examples:

Vacation from 1st of September (provided it's current month) till today:

```
FILL vacation FROM first TO today (07:00-15:30) IN current MONTH WITH 'vacation' COMMENT
```
```
FILL vacation FROM 1 TO today (07:00-15:30) IN September MONTH WITH 'vacation' COMMENT
```
```
FILL vacation FROM 1 TO today (07:00-15:30) IN 9 MONTH WITH 'vacation' COMMENT
```

__Please keep in mind__ that 'today' keyword means not today's exact date (let's say '3rd of November 2015') but today's day number (3rd day of the month). Therefore using 'today' for following months is legal:

```
FILL vacation FROM 1 TO today (07:00-15:30) IN current MONTH WITH ' ' COMMENT
```
```
FILL vacation FROM 1 TO today (07:00-15:30) IN December MONTH WITH ' ' COMMENT
```

__Also__ be sure not to abuse 'first' and 'last' keywords. For example, the following example will cause error:

```
FILL vacation FROM last TO first (07:00-15:30) IN December MONTH WITH ' ' COMMENT
```
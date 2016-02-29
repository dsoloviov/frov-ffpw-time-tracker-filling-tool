# ICS FFPW TIME TRACKER FILLING TOOL

| Author | Email |
| --- | --- |
| Dmytro Soloviov | [dmytro.soloviov@gmail.com](dmytro.soloviov@gmail.com) |

TTFT (Time tracker filling tool) is a tool for automated filling the time tracking sheets of ICS FFPW USB (Institute of Complex Systems, Faculty of Fisheries and Protection of Waters, University of South Bohemia). Tool is based on [Requests](http://docs.python-requests.org/en/master/) library and written in [Python](https://www.python.org/).

### Running

Tool can be started without argument (if __schedule.txt__ and __config.ini__ are available in tool's root directory):

```
python dochazka.py
```

Also it is possible to provide custom schedule file and/or custom config file:

```
python dochazka.py -f %absolute_path_to_schedule_file%
python dochazka.py -c %absolute_path_to_config_file%
python dochazka.py -c %path_1% -f %path_2%
```

Please make sure to provide the appropriate username and password in __config.ini__.

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

TTFT relies on [Requests](http://docs.python-requests.org/en/master/):

```
pip install requests
```

### Configuration file

Configuration file (__config.ini__) contains username and password needed to log in to the tracking system and its full qualified URL. The valid file structure is following:

```
[Credentials]
URL = http://www.auc.cz/ipb/dochazka
Username = your_username
Password = your_password
```

### Creating schedules

TTFT processes scenario from the TXT file (__schedule.txt__) and performs command(s) inside it. The command structure is:

```
FILL activity_type FROM start_date TO end_date (HH:MM-HH:MM)
IN month MONTH WITH 'comment_text' COMMENT
```

__All command from FILL to COMMENT is one line__. Uppercase words are used for parsing the command, do not change them. User have to specify activity type (work, vacation, sick leave, etc.), date range (e.g. from 1st to 15th), time to submit and month. Comments are optional (however, single quotes are required).

Schedule can contain several lines of commands that will be executed one by one, for example let's consider our typical month (just kidding, be healthy):

- work from the beginning of the month to 10th
- vacation from 11th to 20th
- sick leave from 21st to end of the month

These translates into schedule commands as:

```
FILL work FROM first to 10 (07:00-15:30) IN October MONTH WITH 'just regular work' COMMENT
FILL vacation FROM 11 TO 20 (07:00-15:30) IN October MONTH WITH 'vacation' COMMENT
FILL sick FROM 21 TO last (07:00-15:30) IN October MONTH WITH 'sick leave' COMMENT
```

#### Activity types

- 'vacation': Dovolená (vacation)
- 'trip': Služebni cesta (busibess trip)
- 'sick': Nemoc (sick leave)
- 'work': Práce (regular work)
- 'family': Ošetřování člena rodiny
- 'holiday': Jiné volno
- 'dayoff': Nahradní volno (day off)
- 'doctor': Celodenní lekař
- 'other': Indispoziční volno

#### Start / end date:

- number (1 to last day of month, e.g. 31)
- 'yesterday'
- 'today'
- 'tomorrow'
- 'last' - last day of month
- 'first' - first day of month

#### Start / end time:

The format of time is HH:MM-HH:MM. For example, (07:00-18:00) means working from 7AM to 6PM. Hours can be in range from 00 to 23, minutes - from 00 to 50 (with step 10).

#### Month:

Month can be specified as number (1 for January, 12 for December) or using the word: January, June, etc. Also user can use the keyword 'current' to use current month.

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

__Please keep in mind__ that 'today' keyword doesn't mean today's exact date (let's say '3rd of November 2015') but rather today's day number (3rd day of the month). Therefore using 'today' for upcoming months is legal:

```
FILL work FROM 1 TO today (07:00-15:30) IN current MONTH WITH ' ' COMMENT
```
```
FILL work FROM 1 TO today (07:00-15:30) IN December MONTH WITH ' ' COMMENT
```

__Also__ be sure not to abuse 'first' and 'last' keywords. For example, the following example will cause error:

```
FILL vacation FROM last TO first (07:00-15:30) IN December MONTH WITH ' ' COMMENT
```

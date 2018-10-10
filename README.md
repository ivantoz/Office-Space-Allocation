# Amity Room Allocation

[![Build Status](https://travis-ci.org/ivantoz/Office-Space-Allocation.svg?branch=dev)](https://travis-ci.org/ivantoz/Office-Space-Allocation)
[![Coverage Status](https://coveralls.io/repos/github/ivantoz/Office-Space-Allocation/badge.svg?branch=dev)](https://coveralls.io/github/ivantoz/Office-Space-Allocation?branch=dev)

Amity is a room allocation and management system for one of andela's facilities called 'Amity'

**Installation**

`$ git clone -b dev https://github.com/ivantoz/Office-Space-Allocation.git`

`$ cd amity/`

Create and activate a virtual environment

```

$ virtualenv -p /usr/bin/python3 .env
$ source .env/bin/activate

```

Install dependencies
`$ pip install -r requirements.txt`

**Run the application**
```

$ python app.py -i

```


**Run Tests**
```

$ pytest -v --cov=app --cov-report=xml --cov-report=term-missing

```

**Commands**
```

app.py (-i | --interactive)
app.py (-h | --help )
app.py (-v | --version)
Amity$: create_room <room_type> <room_name> ...
Amity$: add_person <employee_number> <first_name> <last_name> <job_type> [wants_accommodation]
Amity$: reallocate_person <person_identifier> <new_room>
Amity$: load_people <filename>
Amity$: print_room <room_name>
Amity$: print_allocations [--o=filename]
Amity$: print_unallocated [--o=filename]
Amity$: load_state [--dbname]
Amity$: save_state [--o=db_name]
Amity$: quit


```
**Description**
- [x] create_room <room_name>... 
 -Creates rooms in Amity. Using this command I should be able to create as many rooms as possible by specifying multiple room names after the create_room command.

- [x] add_person <person_name> <FELLOW|STAFF> [wants_accommodation] - Adds a person to the system and allocates the person to a random room. wants_accommodation here is an optional argument which can be either Y or N. The default value if it is not provided is N.
- [x] reallocate_person <person_identifier> <new_room_name> - Reallocate the person with person_identifier to new_room_name.
- [x] load_people  - Adds people to rooms from a txt file. See data.txt for text input format.
- [x] print_allocations [-o=filename] - Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered allocations to a txt file. See Appendix 2A for format.
- [x] print_unallocated [-o=filename] - Prints a list of unallocated people to the screen. Specifying the -o option here outputs the information to the txt file provided.
- [x] print_room <room_name> - Prints  the names of all the people in room_name on the screen.
- [x] save_state [--db=sqlite_database] - Persists all the data stored in the app to a SQLite database. Specifying the --db parameter explicitly stores the data in the sqlite_database specified.  
- [x] load_state <sqlite_database> - Loads data from a database into the application.

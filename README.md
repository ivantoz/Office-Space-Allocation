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

$ pytest tests/test_amity.py

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

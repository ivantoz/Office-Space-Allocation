"""
Amity Allocator
This system makes it easy to manage rooms and people at Amity.
Usage:
    create_room <room_type> <room_name> ...
    add_person <employee_number> <first_name> <last_name> <job_type> [wants_accommodation]
    reallocate_person <person_identifier> <new_room>
    load_people <filename>
    print_room <room_name>
    print_allocations [--o=filename]
    print_unallocated [--o=filename]
    load_state [--dbname]
    save_state [--o=db_name]
    quit
    (-i | --interactive)
Options:
    -h --help Show this screen.
    -i --interactive Interactive mode.
    -v --version
"""
import cmd

from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint

from app.amity import Amity


def app_exec(func):
    """ Decorator definition for the app."""

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            msg = "Invalid command! See help."
            print(msg)
            print(e)
            return
        except SystemExit:
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityApp(cmd.Cmd):
    intro = cprint(figlet_format("Amity", font="cosmike"), "green")
    prompt = "Amity --> "

    amity = Amity()

    @app_exec
    def do_create_room(self, arg):
        """
        Creates rooms in Amity. Should be able to create as many rooms as possible by specifying multiple room names after the create_room command
        Usage: create_room <room_type> <room_name> ...
        """
        room_type = arg["<room_type>"]
        room_name = arg["<room_name>"]
        self.amity.create_room(room_type, room_name)

    @app_exec
    def do_add_person(self, arg):
        """
        Adds a person to the system and allocates the person to a random room. wants_accommodation here is an optional argument which can be either Y or N
        Usage: add_person <employee_number> <first_name> <last_name> <job_type> [wants_accommodation]
        """
        employee_no = arg["<employee_number>"]
        job_type = arg["<job_type>"]
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        wants_accommodation = arg["wants_accommodation"]
        if wants_accommodation is None:
            wants_accommodation = "N"

        self.amity.add_person(employee_no, first_name, last_name, job_type, wants_accomodation=wants_accommodation)

    @app_exec
    def do_print_room(self, arg):
        """
        Prints  the names of all the people in room_name on the screen.
        Usage: print_room <room_name>
        """
        print(self.amity.print_room(arg["<room_name>"]))

    @app_exec
    def do_print_allocations(self, arg):
        """
        Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered allocations to a txt file.
        Usage: print_allocations [--o=filename]
        """
        filename = arg["--o"] or ""
        self.amity.print_allocations(filename)

    @app_exec
    def do_print_unallocated(self, arg):
        """
        Prints a list of unallocated people to the screen. Specifying the -o option here outputs the information to the txt file provided.
        Usage: print_unallocated [--o=filename]
        """
        filename = arg["--o"] or ""
        self.amity.print_unallocated(filename)

    @app_exec
    def do_load_people(self, arg):
        """
        Adds people to rooms from a txt file.
        Usage: load_people <filename>
        """
        self.amity.load_people(arg["<filename>"])


    @app_exec
    def do_reallocate_person(self, arg):
        """
        Reallocate the person with person_identifier to new_room_name.
        Usage: reallocate_person <person_name> <new_room>
        """
        person_name = arg["<person_name>"]
        new_room = arg["<new_room>"]
        self.amity.reallocate_person(person_name, new_room)

    @app_exec
    def do_load_state(self, arg):

        """
        Loads data from a database into the application
        Usage: load_state <filename>
        """
        self.amity.load_state(arg["<filename>"])

    @app_exec
    def do_save_state(self, arg):
        """
        Persists all the data stored in the app to a SQLite database. Specifying the --db parameter explicitly stores the data in the sqlite_database specified.
        Usage: save_state [--db_name=sqlite_db]
        """
        db = arg['--db_name']
        if db:
            self.amity.save_state(db)
        else:
            self.amity.save_state()

    @app_exec
    def do_quit(self, arg):
        """
        Exits the app.
        Usage: quit
        """
        print("exiting the app ...")
        exit()



if __name__ == '__main__':
	AmityApp().cmdloop()

import index
import datetime


def save():
    with open("records.txt", "w") as file:  # create/open records.txt
        for i in records:  # loop through records(a list)
            file.write(
                f'{i[0]}|{i[1]}|{i[2]}|{i[3]}|{i[4]}|{i[5]}|{i[6]}|{i[7]}|{i[8]}|{i[9]}|{i[10]}\n')  # paste i's various parts to file with | as separator
            # 'with' keyword makes closing file unnecessary


def load():
    try:
        with open("records.txt", "r") as file:  # open records.txt
            for i in file:  # loop through file
                # flight is file that was split into a list and without the \n character
                flight = i[:-1].split("|")
                # flight_list is a list with flight's values
                flight_list = [flight[0], flight[1], flight[2], flight[3],
                               flight[4], flight[5], flight[6], flight[7], flight[8], flight[9], flight[10]]
                # append flight_list to records (a list w/in a list)
                records.append(flight_list)
    except FileNotFoundError:  # if file doesn't exist, just pass
        pass


def no_records_yet():  # return True if records has no content
    return len(records) == 0


def menu():  # print menu, ask and return choice
    print("\nAdmin Options:")
    print("[1] Add a flight")
    print("[2] Edit a flight")
    print("[3] Delete a flight")
    print("[4] View flights")
    print("[5] Search flights")
    print("[6] Go back to user type options")
    print("[0] Exit")
    choice = input("Choice: ")
    print()
    return choice


def admin_main():
    load()  # load first at start of program
    while True:  # continuously print until break is hit
        opt = menu()

        if opt == '1':  # branch out to different function depending on choice
            add_flight()
        elif opt == '2':
            if no_records_yet():  # if records, is empty, just print something
                print("There are no flights to edit yet")
            else:
                edit_flight()
        elif opt == '3':
            if no_records_yet():
                print("There are no flights to delete yet")
            else:
                del_flight()
        elif opt == '4':
            if no_records_yet():
                print("There are no flights to view yet")
            else:
                view_menu()
        elif opt == '5':
            if no_records_yet():
                print("There are no flights to view yet")
            else:
                search_menu()
        elif opt == '6':
            index.index_main()
        elif opt == '0':
            break
        else:
            print("Invalid input")


def flight_id_exists(flight_id):
    list_of_flight_id = [i[0] for i in records]  # list of all flight IDs
    # returns True if parameter is in list above
    return flight_id in list_of_flight_id


def generate_id():
    list_of_flight_id = [i[0] for i in records]  # list of all flight IDs
    if len(list_of_flight_id) == 0:  # if no ids yet, return 0001
        return '0001'
    else:
        list_of_flight_id.sort()  # sort ascendingly
        # add 1 to biggest existing id, eg. 10 -> 11
        init_id = str(int(list_of_flight_id[-1])+1)

        if len(init_id) == 1:  # add leading zeroes depending on length of init_id
            final_id = f'000{init_id}'
        elif len(init_id) == 2:
            final_id = f'00{init_id}'
        elif len(init_id) == 3:
            final_id = f'0{init_id}'
        elif len(init_id) == 4:
            final_id = init_id

        return final_id


def is_valid_date(date):
    try:
        # date_list is a list that came from date being split with '-' as separator
        date_list = [int(i) for i in date.split('-')]

        # create date through datetime library. example output: 2021-12-24
        final = datetime.date(date_list[0], date_list[1], date_list[2])
        # returns True if final is not yesterday or older
        return final >= datetime.date.today()

    # if date being pasted in datetime make an error (eg. if date was 2021-12-), return False
    except (ValueError, IndexError):
        return False


def get_valid_date(type):  # type is either departure or arrival
    while True:  # ask for input until result returns True when passed in is_valid_date
        result = input(f"Date of {type} (yyyy-mm-dd format): ")
        if not is_valid_date(result):
            print("\nInput valid date that follows format.\n")
        else:
            return result


def is_valid_time(time):
    try:
        # str_time_list is a list from time being split with ':' as separator
        str_time_list = time.split(':')
        # if minutes length is only one eg. 3:0, return False
        if len(str_time_list[1]) == 1:
            return False

        # a list with above list's values but in int type
        time_list = [int(i) for i in str_time_list]

        # if no error was triggered from time being pasted in datetime.time, return True
        final = datetime.time(time_list[0], time_list[1])
        return True

    except (ValueError, IndexError):
        return False


def get_valid_time(type):  # type is either departure or arrival
    while True:  # ask for input until result returns True when passed in is_valid_time
        result = input(f"Time of {type} (24-hr format, hh:mm): ")
        if not is_valid_time(result):
            print("\nInput valid time that follows format.\n")
        else:
            return result


def get_datetime(date, time):  # combines date and time in one datetime
    list = [int(i) for i in date.split('-')] + [int(i)
                                                for i in time.split(':')]  # make one list that is a combination of date and time being split

    # formulate final from list's values
    final = datetime.datetime(list[0], list[1], list[2], list[3], list[4])
    return final


def check_datetime_conflict(date1, time1, date2, time2):
    # formulate 2 datetimes through get_datetime function
    final1 = get_datetime(date1, time1)
    final2 = get_datetime(date2, time2)

    return final1 < final2  # return True if final1 is before final2


def seats(n):  # return corresponding string depending on n
    if n == '10':
        # this is a str, not a list. [] is used for separator since it would be put in a txt file
        return '[A1,A2,A3,A4,A5,B1,B2,B3,B4,B5]'
    elif n == '15':
        return '[A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,C1,C2,C3,C4,C5]'


def is_valid_input(inp):  # returns False if inp has , or | or is empty
    if '|' in inp or ',' in inp:
        print("\nIllegal characters detected in the input")
        return False
    elif len(inp) == 0:
        print("\nInput cannot be empty!")
        return False
    return True


def add_flight():
    flight_id = generate_id()  # get id
    print(f"Flight ID: {flight_id}")

    while True:  # continuously ask for input until input becomes valid
        aircraft_name = input("Aircraft name: ").title()
        if is_valid_input(aircraft_name):
            break
    while True:
        depart_loc = input("Departure location: ").title()
        if is_valid_input(depart_loc):
            break
    while True:
        dest_loc = input("Destination location: ").title()
        if is_valid_input(dest_loc):
            break

    # get inputs through pre-made functions
    # note that a date before today is also invalid
    date_depart = get_valid_date("departure")
    time_depart = get_valid_time("departure")

    date_arrival = get_valid_date("arrival")
    time_arrival = get_valid_time("arrival")

    # checks if departure time is before arrival time. if so:
    if check_datetime_conflict(date_depart, time_depart, date_arrival, time_arrival):
        max_passengers = ''
        # ask for max passengers while input is not 10 or 15
        while max_passengers != '10' and max_passengers != '15':
            max_passengers = input("Maximum number of passengers (10 or 15): ")

            if max_passengers != '10' and max_passengers != '15':
                print("\nInvalid input. Enter 10 or 15")

        print("\nSuccessfully added flight!")
        # once there are no input errors, compile inputs to one list then append to records, then save to txt file
        member_record = [flight_id, aircraft_name, depart_loc, dest_loc, date_depart,
                         time_depart, date_arrival, time_arrival, max_passengers, '[]', seats(max_passengers)]
        # '[]' is for list of passengers and their seats. i made a string of [] instead of a list since it would be put in a txt file
        # seats(max_passengers) would be '[A1,A2,..]'. these seats would be removed once passengers take them
        records.append(member_record)
        save()
    else:
        print("\nDeparture datetime should be before arrival datetime!")


def show_passengers(n):  # shows all passengers and corresponding seats of a flight
    # we can't use len(n)== 0 since n is not a list. [] is just a separator. if n has no other contents:
    if n == '[]':
        return 'None yet\n'
    else:  # eg. n = '[(Beam - Seat A4]'
        # remove [], then make a list with ',' as the separator
        fin = n[1: -1].split(',')
        result = '\n'  # start result with new line then just append
        for i in fin:  # for every i in list, append i but without the brackets ()
            result += f"    {i[1:-1]}\n"

        return result


def view_flight_dets(id):
    for i in records:
        if i[0] == id:  # if i[0] is equal to passed parameter, print the details of i through indices
            print(f"\nDetails of Flight {id}")
            print(f"Aircraft Name: {i[1]}")
            print(f"Departure Location: {i[2]}")
            print(f"Destination Location: {i[3]}")
            print(f"Date of Departure: {i[4]}")
            print(f"Time of Departure: {i[5]}")
            print(f"Date of Arrival: {i[6]}")
            print(f"Time of Arrival: {i[7]}")
            print(f"Max Number of Passengers: {i[8]}")
            # to display passengers, use pre-made function
            print(f"Passengers: " + show_passengers(i[9]))


def edit_flight():
    flight_id = input("Enter ID of flight to edit: ")
    if flight_id_exists(flight_id):  # checks if id exists
        view_flight_dets(flight_id)  # first display current flight details

        while True:  # continuously print in case of invalid inputs
            print("Which data to edit?")
            print("[1] Aircraft Name")
            print("[2] Departure Location")
            print("[3] Destination Location")
            print("[4] Date of Departure")
            print("[5] Time of Departure")
            print("[6] Date of Arrival")
            print("[7] Time of Arrival")
            print("[0] Discard Edit")
            choice = input("Choice: ")

            choice_dict = {  # dict to show what the corresponding value is
                '1': 'Aircraft Name',
                '2': 'Departure Location',
                '3': 'Destination Location',
                '4': 'Date of Departure',
                '5': 'Time of Departure',
                '6': 'Date of Arrival',
                '7': 'Time of Arrival'
            }

            if choice == '0':  # break out of loop if 0 is selected
                break
            elif choice in ('1', '2', '3', '4', '5', '6', '7'):  # if in 1-7, ask for new value
                new = input(f"Enter new {choice_dict[choice]}: ").title()

                for i in records:  # first find flight in records
                    if i[0] == flight_id:
                        # checks if choice is time or date and if it is a valid time or date
                        if (choice == '4' and not is_valid_date(new)) or (choice == '5' and not is_valid_time(new)) or (choice == '6' and not is_valid_date(new)) or (choice == '7' and not is_valid_time(new)):
                            # note that a date before today is also invalid
                            print("\nInvalid input")

                        # checks if new is just the same as pre-existing value
                        elif new == i[int(choice)]:
                            print("\nNew is just the same as the old one.")

                        else:
                            no_time_conflict = False  # these 2 bool values assess if inputs are invalid
                            valid = False
                            # note that 4-7 are date or time
                            if choice in ('4', '5', '6', '7'):
                                if choice == '4' and check_datetime_conflict(new, i[5], i[6], i[7]):
                                    no_time_conflict = True
                                # checks if new date or time value would cause the departure datetime to be after arrival datetime, which is invalid
                                elif choice == '5' and check_datetime_conflict(i[4], new, i[6], i[7]):
                                    no_time_conflict = True  # if no conflicts, set bool var to true

                                elif choice == '6' and check_datetime_conflict(i[4], i[5], new, i[7]):
                                    no_time_conflict = True

                                elif choice == '7' and check_datetime_conflict(i[4], i[5], i[6], new):
                                    no_time_conflict = True
                            else:  # in the case that the choice is 1-3, which are text inputs:
                                # there is no time conflict since it is just text eg. aircraft name
                                no_time_conflict = True
                                # checks if new has , | or is empty
                                if is_valid_input(new):
                                    valid = True

                            if (no_time_conflict and choice in ('4', '5', '6', '7')) or (valid and choice in ('1', '2', '3')):
                                # if there are no conflicts, put new value in records then save to put it in txt file too
                                i[int(choice)] = new
                                print("\nEdit successful!")
                                save()

                            elif not no_time_conflict:  # if departure datetime becomes later than arrival, print conflict detail
                                print(
                                    "\nDeparture datetime should be before arrival datetime!")

                break  # after edit or conflicts, go back to menu

            else:
                print("\nInvalid input")

    else:
        print("Flight does not exist.")


def del_flight():
    flight_id = input("Enter ID of flight to delete: ")  # ask for id to delete
    if flight_id_exists(flight_id):  # check if id exists
        for i in records:  # find id in records
            if i[0] == flight_id:
                records.remove(i)  # remove flight upon finding it
                print("Flight successfully deleted.")
                save()  # save to update txt file
    else:
        print("Flight does not exist.")


def bubble_sort():  # would be used to sort datetimes
    list = [
        (get_datetime(i[4], i[5]), i[0]) for i in records]  # make a list of datetimes and id's of all record entries through list comprehension
    # indices 4 and 5 are for departure date and time while 0 is for id
    # if list has 5 contents, we would need to iterate 5 times. to do this, though, we would use indices of 4 to 0.
    for i in range(len(list)-1, 0, -1):  # value of i: 4->3->2->1
        for j in range(i):  # for each j, we need to iterate depending on current value of i. for instance, in the first outer iteration, if len(list) == 5 we would iterate internally 4 times. next, we would iterate 3 times. this is because the last values of the list are already sorted.
            if list[j][0] > list[j+1][0]:  # if datetime of j is after datetime of j+1
                list[j], list[j+1] = list[j+1], list[j]  # swap their values

    return list


def view_by_dept_time():
    list = bubble_sort()  # list contains sorted datetimes with their corresponding ids

    print("\nFlights sorted by datetime:")

    for i in list:
        # i[1] is the id while i[0] is the datetime
        print(f"    Flight {i[1]} — {i[0]}")

    post_view_menu()  # call this function after printing flights


def view_by_dept_loc():
    # list of all departure locations
    list_of_dept_loc = sorted(list(set([i[2] for i in records])))
    # set eliminates all duplicates then is made a list again. sorted() sorts the locations alphabetically
    for i in list_of_dept_loc:  # loop through locations
        print(f"\n{i}:")  # print location
        for j in records:  # loop through all flights
            if j[2] == i:  # if flight's dept location is same as i:
                print(f"    Flight {j[0]}")  # print j's id

    post_view_menu()


def view_by_aircraft_name():  # exactly the same logic as view_by_dept_loc but instead of departure location, we use aircraft names
    list_of_aircrafts = sorted(list(set([i[1] for i in records])))

    for i in list_of_aircrafts:
        print(f"\n{i}:")
        for j in records:
            if j[1] == i:
                print(f"    Flight {j[0]}")

    post_view_menu()


def post_view_menu():  # is called after every view or search functions
    choice = ''
    while choice not in ('1', '2'):  # print until choice becomes 1 or 2
        print("\nOptions:")
        print("[1] View more details about a flight")
        print("[2] Go back to menu")
        choice = input("Choice: ")

        if choice == '1':
            flight_id = input("\nEnter flight ID: ")
            if flight_id_exists(flight_id):  # check if flight exists
                view_flight_dets(flight_id)  # print flight details
                # empty input to have separator before printing menu
                input("Press ENTER to go back to menu")

            else:
                print("\nFlight does not exist!")
                post_view_menu()

        elif choice == '2':
            pass
        else:
            print("\nInvalid input")


def view_menu():
    choice = ''
    # print view menu until a valid input is entered
    while choice not in ('1', '2', '3', '0'):
        print("View Options:")
        print("[1] View all flights sorted by Departure Time")
        print("[2] View all flights using Departure Location")
        print("[3] View all flights using Aircraft Name")
        print("[0] Cancel")
        choice = input("Choice: ")

        if choice == '1':  # branch out to other functions depending on user input
            view_by_dept_time()
        elif choice == '2':
            view_by_dept_loc()
        elif choice == '3':
            view_by_aircraft_name()
        elif choice == '0':
            pass
        else:
            print("\nInvalid input\n")


def search_menu():  # same logic as view_menu
    choice = ''
    while choice not in ('1', '2', '3', '0'):
        print("Search Options:")
        print("[1] All flights with available seats")
        print("[2] All flights of an aircraft")
        print("[3] All flights of a day")
        print("[0] Cancel")
        choice = input("Choice: ")

        if choice == '1':
            search_avail_seats()
        elif choice == '2':
            search_aircraft()
        elif choice == '3':
            search_day()
        elif choice == '0':
            pass
        else:
            print("\nInvalid input\n")


def search_avail_seats():
    with_avail_seats = []  # declare empty list
    for i in records:  # since the value of records is from a txt file, the loaded [] is interpreted as '[]'
        if i[-1] != '[]':  # if the last item of i is not '[]', append i's id to above list
            with_avail_seats.append(i[0])

    if len(with_avail_seats) == 0:  # print statement if with_avail_seats is empty
        print("\nThere are no flights with available seats")

    else:
        print("\nFlights with available seats:")
        for j in with_avail_seats:  # if list is not empty, loop through contents and print id
            print(f"    Flight {j}")

        post_view_menu()


def search_aircraft():
    # list of all aircraft names
    list_of_aircrafts = sorted(list(set([i[1] for i in records])))
    # set eliminates all duplicates then is made a list again. sorted() sorts the names alphabetically
    # ask for item to search then title() for match consistency
    aircraft = input("Enter name of aircraft to search: ").title()
    if aircraft in list_of_aircrafts:  # if aircraft exists:
        print(f"\n{aircraft}:")
        for j in records:  # loop through all records and print id if aircraft name matches
            if j[1] == aircraft:
                print(f"    Flight {j[0]}")

        post_view_menu()
    else:  # if aircraft is not in list of all aircrafts, either aircraft does not exist or has no logged flights
        print("\nAircraft does not exist or have no flights booked")


def search_day():  # same logic as search_aircraft but date instead
    list_of_departs = sorted(list(set([i[4] for i in records])))
    depart = input(
        "Enter departure date to search (yyyy-mm-dd format): ")
    if depart in list_of_departs:
        print(f"\nFlights on {depart}:")
        for j in records:
            if j[4] == depart:
                print(f"    Flight {j[0]}")

        post_view_menu()

    elif not is_valid_date(depart):
        # note that a date before today is also invalid
        print("\nInvalid date!")

    else:  # if date is valid but is not in list, there are no logged flights
        print("\nNo flights booked on that date")


records = []  # declare list where data from txt file would be loaded
if __name__ == '__main__':  # prevents admin.py from being ran from simply being imported
    admin_main()

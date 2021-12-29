import index
import admin


def menu():  # print menu, ask and return choice
    print("\nPassenger Options:")
    print("[1] View flights")
    print("[2] Book a flight")
    print("[3] Go back to user type options")
    print("[0] Exit")
    choice = input("Choice: ")
    print()
    return choice


def view_menu_passenger():  # cant be imported from admin since 3 from menu is different
    choice = ''
    # print view menu until a valid input is entered
    while choice not in ('1', '2', '3', '0'):
        print("View Options:")
        print("[1] View all flights sorted by Departure Time")
        print("[2] View all flights using Departure Location")
        print("[3] View all flights using Departure and Destination Locations")
        print("[0] Cancel")
        choice = input("Choice: ")

        if choice == '1':  # branch out to other functions depending on user input
            admin.view_by_dept_time()  # use dot notation to call functions from different files
        elif choice == '2':
            admin.view_by_dept_loc()
        elif choice == '3':
            view_by_dept_dest_loc()  # function that is declared in this file
        elif choice == '0':
            pass
        else:
            print("\nInvalid input\n")


def view_by_dept_dest_loc():
    list_of_loc = sorted(
        list(set([(i[2], i[3]) for i in admin.records])))  # list of all departure to arrival locations in tuple formats

    for i in list_of_loc:  # loops through list
        print(f"\nFlights from {i[0]} to {i[1]}:")
        for j in admin.records:  # loop through records
            # if departure and arrival locations are the same, print id
            if j[2] == i[0] and j[3] == i[1]:
                print(f"    Flight {j[0]}")

    admin.post_view_menu()


# legend is a list containing ✓ or ☓ that is sorted from a1 to b5. this is for when there are only 10 seats
def print_seats_10(legend):
    # print seats with either a ✓ or ☓ to depict whether seat is taken or not
    print('╷———————————————╷')
    print(f'│{legend[0]}  A1  │{legend[5]}  B1  │')
    print('│———————————————│')
    print(f'│{legend[1]}  A2  │{legend[6]}  B2  │')
    print('│———————————————│')
    print(f'│{legend[2]}  A3  │{legend[7]}  B3  │')
    print('│———————————————│')
    print(f'│{legend[3]}  A4  │{legend[8]}  B4  │')
    print('│———————————————│')
    print(f'│{legend[4]}  A5  │{legend[9]}  B5  │')
    print('╵———————————————╵')
    print("Legend:\n    ✓ — Available Seat\n    ☓ — Not Available")


def print_seats_15(legend):  # same logic as above but this is for 15 seats
    print('╷———————————————————————╷')
    print(f'│{legend[0]}  A1  │{legend[5]}  B1  │{legend[10]}  C1  │')
    print('│———————————————————————│')
    print(f'│{legend[1]}  A2  │{legend[6]}  B2  │{legend[11]}  C2  │')
    print('│———————————————————————│')
    print(f'│{legend[2]}  A3  │{legend[7]}  B3  │{legend[12]}  C3  │')
    print('│———————————————————————│')
    print(f'│{legend[3]}  A4  │{legend[8]}  B4  │{legend[13]}  C4  │')
    print('│———————————————————————│')
    print(f'│{legend[4]}  A5  │{legend[9]}  B5  │{legend[14]}  C5  │')
    print('╵———————————————————————╵')
    print("Legend:\n    ✓ — Available Seat\n    ☓ — Not Available")


def book():
    # ask for id to book for
    flight_id = input("Enter flight ID to book for: ")
    if admin.flight_id_exists(flight_id):  # check if id exists

        for i in admin.records:  # loop through records to find flight
            if i[0] == flight_id:
                legend = []  # declare empty list
                # note that i[-1] originally is a list containing 'A1','A2',...
                avail = i[-1][1:-1].split(",")
                # avail is a list containing all available seats since once a seat is booked, it is removed from i[-1]
                all_seats_10 = ['A1', 'A2', 'A3', 'A4',
                                'A5', 'B1', 'B2', 'B3', 'B4', 'B5']
                all_seats_15 = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1',
                                'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5']

                if avail == ['']:  # if avail is reduced to [''] already, it is fully booked
                    print("\nThere are no available seats")

                else:
                    if i[8] == '10':  # if i's max_passenger is 10:
                        for j in all_seats_10:  # loop through all_seats_10
                            if j in avail:  # if j is in avail, append ✓ else ☓
                                legend.append("✓")
                            else:
                                legend.append("☓")
                        # call function and pass legend as parameter
                        print_seats_10(legend)

                    elif i[8] == '15':  # same logic as above but for 15 seats
                        for j in all_seats_15:
                            if j in avail:
                                legend.append("✓")
                            else:
                                legend.append("☓")

                        print_seats_15(legend)

                    while True:
                        # ask for seat then upper() to match case
                        seat = input("\nEnter desired seat: ").upper()
                        # if seat is a real seat eg. A1 but is not in avail, that means it is taken
                        if seat not in avail and ((i[8] == '10' and seat in all_seats_10) or (i[8] == '15' and seat in all_seats_15)):
                            print("\nSeat is taken!")
                        elif seat in avail:  # if seat is in avail:
                            while True:  # print until a valid name is entered
                                # ask for user's name
                                name = input("Enter your name: ").title()
                                # check if valid (no , | and not empty)
                                if admin.is_valid_input(name):
                                    break

                            # example of i[9] is [(Beam - Seat A1), (Railey - Seat A2)]
                            list_of_passengers = i[9][1:-1].split(',')
                            # list_of_passengers removes the []  then splits based on ,
                            # if being split made it [''], make it an empty list
                            if list_of_passengers == ['']:
                                list_of_passengers = []

                            list_of_passengers.append(
                                f"({name} - Seat {seat})")  # append entered name and seat wrapped in brackets
                            # update i[9] through join function
                            i[9] = f'[{",".join(list_of_passengers)}]'

                            # now that seat is taken, remove from avail
                            avail.remove(seat)
                            # update i[10] through join function
                            i[10] = f'[{",".join(avail)}]'

                            admin.save()  # save to update txt file
                            print("\nBooking successful!")
                            break
                        else:
                            print("\nInvalid input")
                            break

    else:
        print("\nFlight does not exist")


def passenger_main():
    # note that i used the records list from the other file as well.
    admin.load()
    while True:  # print menu until 0 is chosen
        opt = menu()

        if opt == '1':  # branch out to different function depending on choice
            if admin.no_records_yet():  # if records, is empty, just print something
                print("There are no flights to view yet")
            else:
                view_menu_passenger()
        elif opt == '2':
            if admin.no_records_yet():
                print("There are no flights to edit yet")
            else:
                book()
        elif opt == '3':
            index.index_main()
        elif opt == '0':
            break
        else:
            print("Invalid input")


if __name__ == '__main__':  # prevents passenger.py from being ran from simply being imported
    passenger_main()

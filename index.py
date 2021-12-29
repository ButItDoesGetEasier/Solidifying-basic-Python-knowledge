# this file is the one to run first
import admin  # imports since program is modularized
import passenger


def index_main():
    print("Welcome to PyFlights!")
    print("Enter user type:")
    print("[1] Admin")
    print("[2] Passenger")

    choice = ''
    while choice != '1' and choice != '2':  # while choice is not 1 or 2, ask for Choice
        choice = input("Choice: ")

        if choice == '1':
            admin.admin_main()  # use dot notation for calling functions from other files
        elif choice == '2':
            passenger.passenger_main()
        else:
            print("Invalid input. Enter '1' or '2'")


if __name__ == '__main__':  # prevents index.py from being ran from simply being imported
    index_main()

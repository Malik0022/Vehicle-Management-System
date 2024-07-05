# # imports start here # #
from person import User
from model import Vehicle,Car
import os
# # imports end here # #

Vehicle.vehicle_validate_path()
User.validate_user_path()

while True:

    Vehicle.display_menu()
    option = input("Choose an option: ")
   
    if option == "1":
        Car.add_car_details()

    elif option == "2":
        User.add_user()
    
    elif option == "3":

        username = input("Enter username to view vehicle details: ").upper()
        vehicle = Vehicle.search_vehicle_csv(username)
        car = Car.search_vehicle_json(username)
        
        if vehicle and car:
            print("Vehicle Found:", vehicle,car)
        else:
            print("Vehicle Not Found")

    elif option == "4":

        username = input("Enter username to search: ").upper()
        user_csv = User.search_user_csv(username)
        user_json = User.search_user_json(username)

        if user_csv and user_json:
            print("User Found:", user_csv,user_json)
        else:
            print("User not found")
    
    elif option == "5":

        updated_vehicle = input("Enter registration no of vehicle to update: ").upper()
        Vehicle.update_vehicle_csv(updated_vehicle)
        # Vehicle.update_vehicle_json(updated_vehicle)
    
    elif option == "6":

        reg_no = input("Enter registration no of vehicle you want to delete: ").upper()
        Vehicle.delete_vehicle(reg_no)
    
    
    elif option == "7":
        
        username = input("Enter username of user you want to delete: ").upper()
        User.delete_user_csv(username)

    elif option == "8":
        os.system("clear")
    
    elif option == "9":
        print("Exiting the program!")
        break

    else:
        print("Invalid choice or number")
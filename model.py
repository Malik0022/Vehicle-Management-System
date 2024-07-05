# imports start here #
import os,csv,json
import smtplib
# imports ends here #

CSV_FILENAME = "vehicles.csv"
JSON_FILENAME = "vehicles.json"
HEADER_ROW = ["Registration No#","Brand","Name","Colour","Transmission_type","Engine_Capacity","Seats","Body_Type","Username"]

class Vehicle:

    def __init__(self, reg_no, brand, name, colour,username=None):

        self.reg_no = reg_no
        self.brand = brand
        self.name = name
        self.colour = colour
        self.username = username
        
    
    @staticmethod
    def display_menu():

        print("\nMenu:")
        print("1. Add a vehicle details")
        print("2. Add a username details")
        print("3. Search a vehicle by username to see vehicle's details")
        print("4. Search a username to see user's details")
        print("5. Update a vehicle")
        print("6. Delete a vehicle details")
        print("7. Delete a user's details")
        print("8. Clears console")
        print("9. Exit the program!")

    @staticmethod
    def vehicle_validate_path():

        if not os.path.exists(CSV_FILENAME):
            open(CSV_FILENAME,"x").close()
            with open(CSV_FILENAME,"w") as file:
                writer = csv.writer(file)
                writer.writerow(HEADER_ROW)

        if not os.path.exists(JSON_FILENAME):
            with open(JSON_FILENAME,"w") as file:
                json.dump([],file)
    
    def write_to_csv(vehicle, filename = CSV_FILENAME):

        with open(filename, "a", newline='') as file:
            writer = csv.writer(file)
            if isinstance(vehicle, Car):
                writer.writerow([vehicle.reg_no, vehicle.brand, vehicle.name, vehicle.colour, vehicle.transmission_type, vehicle.engine_capacity, vehicle.seats, vehicle.body_type, vehicle.username])
            else:
                writer.writerow([vehicle.reg_no, vehicle.brand, vehicle.name, vehicle.colour, "", "", "", "", vehicle.username])

    def write_to_json(vehicle, filename=JSON_FILENAME):
        
        vehicle_data = {
            "reg_no": vehicle.reg_no,
            "brand": vehicle.brand,
            "name": vehicle.name,
            "colour": vehicle.colour,
            "username": vehicle.username
        }
        
        if isinstance(vehicle, Car):
            vehicle_data.update({
                "transmission_type": vehicle.transmission_type,
                "engine_capacity": vehicle.engine_capacity,
                "seats": vehicle.seats,
                "body_type": vehicle.body_type
            })
        
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(vehicle_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
 
    @staticmethod
    def search_vehicle_csv(username: str):

        results = []
        with open(CSV_FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[-1].upper() == username.upper():
                    results.append(row)
        return results
    
    @staticmethod
    def search_vehicle_json(username: str):

        results = []
        with open(JSON_FILENAME,"r") as file:
            data = json.load(file)
            for row in data:
                if row["username"].upper() == username.upper():
                    results.append(row)
        return results

    @staticmethod
    def delete_vehicle_csv(reg_no: str):

        vehicles = []

        with open(CSV_FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != reg_no:
                    vehicles.append(row)

        with open(CSV_FILENAME, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(vehicles)

        print("Vehicle deleted successfully.")
    
    @staticmethod
    def update_vehicle_csv(reg_no:str):

        vehicles = []
        found = False
        with open(CSV_FILENAME,"r") as file:
            reader = csv.reader(file)
            headers = next(reader)
        
            for row in reader:

                if row[0] == reg_no:
                    update_options = {
                        1: "Brand",
                        2: "Name",
                        3: "Colour",
                        4: "Username"
                    }
                    print("Current Details",row)
                    to_update = input("What do you want to update: \n1. Brand,\n2. Name,\n3. Color,\n4. Username,\nEnter [1-3]: ")
                    data_to_update = update_options[int(to_update)]

                    new_value = input(f"Enter {data_to_update}: ")

                    if data_to_update in headers:
                        index = headers.index(data_to_update)
                        row[index] = new_value
                        found = True

                    else:
                        print("Invalid field.")
                vehicles.append(row)

    
        if found:
            with open(CSV_FILENAME, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  
                writer.writerows(vehicles) 

            Vehicle.update_vehicle_json(reg_no) 
            print("Vehicle details updated successfully.")

        else:

            print("Vehicle not found.")
    
class Car(Vehicle):

    def __init__(self,reg_no, brand, name, colour,transmission_type,engine_capacity,seats,body_type,email,username=None):
        super().__init__(reg_no, brand, name, colour, username)
        self.transmission_type = transmission_type
        self.engine_capacity = engine_capacity
        self.seats = seats
        self.body_type = body_type
        self.email = email

    def email_registration(self):

        reciever_email = self.email
        subject = "Car Registration Information"
        body = (
            f"Respected {self.username}!,\n\n"
            f"I hope this message finds you well. As discussed, I am providing you with the necessary information regarding the car registration for the {self.brand} {self.name} that you are purchasing from me. Below are the details:\n\n"
            f"Registration No: {self.reg_no}\n"
            f"Brand: {self.brand}\n"
            f"Name: {self.name}\n"
            f"Color: {self.colour}\n"
            f"Transmission Type: {self.transmission_type}\n"
            f"Engine Capacity: {self.engine_capacity}\n"
            f"Seats: {self.seats}\n"
            f"Body Type: {self.body_type}\n\n"
            f"Please ensure that you have all the required documents and information for the transfer of registration. If you have any questions or need further assistance regarding this matter, feel free to contact me.\n\n"
            "Thank you for your attention to this. I look forward to completing the transaction smoothly.\n\n"
            "Best regards,\n"
            "Muhammad Saim\n"
            "03146255409"
        )

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login("smaliksaim@gmail.com", "wptw jtdr redu rdyg")
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail("smaliksaim@gmail.com",reciever_email, message)
            print(f"Registration email sent to {self.email} successfully!.")
            server.quit()
            
        except Exception as e:
            print(f"Failed to send email: {e}")
       
    @staticmethod
    def add_car_details():

        username = input("Username: ")
        email = input("Email: ")
        reg_no = input("Registration no#: ")
        brand = input("Brand: ")
        name = input("Name: ")
        colour = input("Colour: ")
        transmission_type = input("Transmision_type: ")
        engine_capacity = input("Engine_capacity: ")
        seats = input("Seats: ")
        body_type = input("Body_type: ")
        car_details = Car(reg_no,brand,name,colour,transmission_type,engine_capacity,seats,body_type,email,username)
        Car.write_to_csv(car_details)
        Car.write_to_json(car_details)
        Car.email_registration(car_details)
        print("Car details added successfully")
    

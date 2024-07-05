# # imports start here # #
import csv,os,json
# # imports ends here # #

JSON_FILENAME = "users.json"
CSV_FILENAME = "users.csv"
HEADER_ROW = ["Username", "Email", "Phone", "City"]

class User:

    def __init__(self, username, email, phone, city):

        self.username = username
        self.email = email
        self.phone = phone
        self.city = city

    @staticmethod
    def validate_user_path():

        if not os.path.exists(CSV_FILENAME):
            open(CSV_FILENAME, "x").close()
            with open(CSV_FILENAME, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(HEADER_ROW)
        
        if not os.path.exists(JSON_FILENAME):
            with open(JSON_FILENAME,"w") as file:
                json.dump([],file)
              

    @staticmethod
    def add_user():

        username = input("Enter Username: ").upper()
        email = input("Enter Email: ")
        phone = input("Enter Phone: ")
        city = input("Enter City: ")
        user = User(username, email, phone, city)
        User.write_user_to_csv(user)
        User.write_user_to_json(user)
        print("User added successfully.")

    
    def write_user_to_csv(user: str, filename: str = CSV_FILENAME):

        with open(filename, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user.username, user.email, user.phone, user.city])
    
   
    @staticmethod
    def search_user_csv(username: str):

        with open(CSV_FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].upper() == username:
                    return row
        return None


    @staticmethod
    def delete_user_csv(username:str):
        
        user = []

        with open(CSV_FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != username:
                    user.append(row)

        with open(CSV_FILENAME, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(user)

        print("User deleted successfully.")

    def write_user_to_json(user, filename=JSON_FILENAME):

            # isme data store kreingy jo load hoga json file sy
            users = []

            # file read kreingy
            with open(filename, "r") as file:
                users = json.load(file)

        
            user_data = {

                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "city": user.city
            }

            users.append(user_data)

            
            with open(filename, "w") as file:
                json.dump(users, file, indent=4)

    @staticmethod
    def search_user_json(username:str):
        
        with open(JSON_FILENAME,"r") as file:
            users = json.load(file)
            for row in users:
                if row["username"].upper() == username:
                    return row
        return None

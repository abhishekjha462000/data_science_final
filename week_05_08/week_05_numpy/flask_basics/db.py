import json

class Database:
    
    def insert(self, name, email, password):
        # open the users.json file in read mode
        # add the data in the users.json file

        with open("users.json", "r") as rf:
            users = json.load(rf)

            if email in users:
                return 0
            else:
                users[email] = [name, password]
        
        # now dump this users variable into the users.json file
        with open("users.json", "w") as wf:
            json.dump(users, wf)
            return 1

    
    def search(self, email, password):
        # open the users.json file in read mode
        with open("users.json", "r") as rf:
            users = json.load(rf)

            if email in users:
                if password == users[email][1]:
                    return 1
                return 0
            else:
                return 0

    def find_user_name(self, email, password):
        # open the users.json file in read mode
        with open("users.json", "r") as rf:
            users = json.load(rf)

            if email in users:
                if password == users[email][1]:
                    return users[email][0] # name of the user if found successfully
        
        return None # if the user email does not exist or if the password is wrong then we return None.
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
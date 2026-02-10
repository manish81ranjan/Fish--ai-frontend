from extensions import mongo

def create_user(name, email, password):
    return mongo.db.users.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

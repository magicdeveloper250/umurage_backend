import bcrypt 
password= "password123".encode()
print(bcrypt.hashpw(password, bcrypt.gensalt()))

import requests
import bcrypt

# image = requests.get(
#     "https://recruitment.mifotra.gov.rw/api/external/verify-nid-number/1197970051236064"
# )
# print(image.content)
hashed_pw=bcrypt.hashpw(
            "password123.".encode(), bcrypt.gensalt()
        )
print(hashed_pw)

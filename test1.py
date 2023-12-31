# from datetime import datetime as datetime_object

# import datetime

# date = datetime_object(year=2023, month=12, day=31)
# now_date = datetime_object.now().date()
# new_date = datetime_object(year=now_date.year, month=now_date.month, day=now_date.day)
# # compare two dates
# print(date < new_date)

import bcrypt

password = "RU6w&2s-9ZT44wr"
hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashedpw)
print(str(hashedpw).removeprefix("b'").removesuffix("'"))

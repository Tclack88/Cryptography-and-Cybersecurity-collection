Room: https://tryhackme.com/room/owasptop102021

Databases are best handled securely by connecting to a database server. If they're stored locally as files (flat-file databases), then it can be found and is vulnerable. Consider the file 'webapp.db' found in the home location of a webapp. We can download and open with sqlite3 (we know this based on checking the type from terminal):

sqlite> .tables
sessions  users   
sqlite> select * from users;
4413096d9c933359b898b6202288a650|admin|6eea9b7ef19179a06954edd0f6c05ceb|1
23023b67a32488588db1e28579ced7ec|Bob|ad0234829205b9033196ba818f7a872b|1
4e8423b514eef575394ff78caed3254d|Alice|268b38ca7b84f44fa0a6cdc86e6301e0|0

here, we have the hashed passwords. 32 characters, probably md5sum. Check with python:

import hashlib

```python3
password_sources = '/home/tclack/workshop/hproj/picoCTF/heresjohnny/rockyou.txt'
hashed = '6eea9b7ef19179a06954edd0f6c05ceb' # admin password

with open(password_sources, errors='ignore') as source:
    for line in source:
        password = line[:-1]
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        if hashed_pw == hashed:
            print(password) # returns qwertyuiop
            break
```

(Can also take the easy way out and use [Crackstation](https://crackstation.net/))



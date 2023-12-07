import hashlib

password_sources = '/home/tclack/workshop/hproj/picoCTF/heresjohnny/rockyou.txt'
hashed = '6eea9b7ef19179a06954edd0f6c05ceb' # admin password

with open(password_sources, errors='ignore') as source:
    for line in source:
        password = line[:-1]
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        if hashed_pw == hashed:
            print(password)
            break

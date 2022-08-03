#!/usr/bin/env python
from socket import *
from functions import *
import getpass



s = socket(AF_INET, SOCK_STREAM)

s.connect(("127.0.0.1",143))
a = s.recv(1024)

a = a.decode()
if("* OK" in  a):
	print("Socket Connection Successfull")
	username = input("Username: ")
	password = getpass.getpass("Password: ")
	login(s,username,password)
else:
	print("Try Again")


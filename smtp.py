#!/usr/bin/env python
from socket import *


def compose():
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(("127.0.0.1",25))
	a = s.recv(1024)
	fro = input("FROM: ")
	fro = "MAIL FROM: <"+fro+">\r\n"
	s.send(fro.encode())
	fro = s.recv(4096).decode()
	if('Ok' in fro):
		pass
	else:
		print("Something went wrong")
		return
	to = input("TO: ")
	to = "RCPT TO: <"+to+">\r\n"
	s.send(to.encode())
	to = s.recv(4096).decode()
	if('Ok' in to):
		pass
	else:
		print("Something went wrong")
		return
	k = "DATA\r\n"
	s.send(k.encode())
	k = s.recv(1024)
	sub = input("Subject: ")
	sub = "Subject: "+sub+"\r\n"
	s.send(sub.encode())
	s.send('\r\n'.encode())
	print("Body (end with .)")
	text = ""
	while(1):
		k = input()
		if(k == '.'):
			text+="\r\n"
			break
		else:
			text += k
	k+='\r\n'
	s.send(text.encode())
	s.send(k.encode())
	k = s.recv(1024).decode()
	return
		
		

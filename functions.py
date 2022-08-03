#!/usr/bin/env python
from socket import *
from smtp import *
import time
from os import system


def logout(s):
	l = "e logout\r\n"
	s.send(l.encode())
	l = s.recv(4096).decode()
	if('BYE' in l):
		print("Logged out")
		system('clear')
		exit()
		return
	
def parse(fch):
	fch = fch.split('(')
	date = fch[3]
	date = list(date)
	if("\""in date):
		date.remove("\"")
	date = ''.join(date)
	sub = fch[4]
	sub = sub.split(' ')
	sub = sub[1:6]
	sub = list(' '.join(sub))
	if("\""in sub):
		sub.remove("\"")
	if("\""in sub):
		sub.remove("\"")
	sub= ''.join(sub)
	fro = parse_from(fch[6])
	return [date,sub,fro]
	

def parse_to(fch):
	to1 = fch.split(' ')
	if(to1[0] == "NIL"):
		pass
	else:
		t = to1[0]
		t = list(t)
		if("\"" in t):
			t.remove("\"")
		if("\"" in t):
			t.remove("\"")
		to1[2] = to1[0] + " <" + to1[2] 
		to1[3] += ">"
	to = to1[2]
	to += '@'
	to += (to1[3])
	to = list(to)
	for i in to:
		if(i == "\"" or i == ")"):
			to.remove(i)
	if(")"in to):
		to.remove(')')
	to = ''.join(to)
	return to

def parse_from(fch):
	fro = fch
	fro = fro.split(' ')
	for i in range(len(fro)):
		j = list(fro[i])
		for k in j:
			if(k == "\"" or k == ')'):
				j.remove(k)
		fro[i] = ''.join(j)
		if(fro[i] == 'NIL' and ' <' not in fro):
			fro[i] = ' <'
		elif(fro[i] == 'NIL'):
			fro[i] = ""
	fro.insert(3,'@')
	fro = ''.join(fro)
	fro = list(fro)
	if(")" in fro): 
		fro.remove(')')
	fro.append('>')
	fro = ''.join(fro)
	return fro
		


def parse_dateSub(fch):
	date = subject = fch
	l = date.split(' ')
	subject = str(' '.join(l[6:]))
	date = str(' '.join(l[:6]))
	subject = list(subject)
	subject.remove(date[0])
	subject.remove(date[-1])
	d = list(date)
	d.remove(date[0])
	d.remove(date[-1])
	return [''.join(d),''.join(subject)]



def parsing_mail(fch):
	fch = fch.split('(')
	date = fch[3]
	date = list(date)
	if("\"" in date): 
		date.remove("\"")
	date = ''.join(date)
	sub = fch[4]
	sub = sub.split(' ')
	sub = sub[1:6]
	sub = list(' '.join(sub))
	if("\""in sub):
		sub.remove("\"")
	if("\""in sub):
		sub.remove("\"")
	sub= ''.join(sub)
	fro = parse_from(fch[6])
	to = parse_to(fch[12])
	return [date,sub,fro,to]

def fetch(s,number_of_mails):
	n = 1
	while(n <= number_of_mails):
		system('clear')
		fch = "2 FETCH "+str(n)+" FULL \r\n"
		s.send(fch.encode())
		fch = s.recv(4096).decode()
		if("Mail Delivery System" in fch):
			r = parsing_mail(fch)
			date = r[0]
			sub = r[1]
			fro = r[2]
			to = r[3]
		elif(len(fch.split('(')) == 14):
			r = parse(fch)
			fro = r[2]
			date = r[0]
			sub = r[1]
			to = 0
		elif(len(fch.split('(')) == 15):
			fch = fch.split('(')
			to = parse_to(fch[11])
			fro = parse_from(fch[5])
			dat_sub = parse_dateSub(fch[3])
			date = dat_sub[0]
			sub = dat_sub[1]
		print("Date:",date)
		print("From:",fro)
		if(to):
			print("To:",to)
		print("Subject:",sub)
		fch = "2 FETCH "+str(n)+" BODY[TEXT] \r\n"
		s.send(fch.encode())
		fch = s.recv(4096).decode()
		fch = fch.split('\n')
		fch.remove(fch[0])
		fch = fch[:-3]
		fch = '\n'.join(fch)
		print("\n"+fch+"\n")
		print("n : next ; p : previous ; d:delete ; c : compose ; q : quit")
		k = input('')
		if(k == 'p'):
			n = n-1
		elif(k == 'n'):
			n = n+1
		elif(k == 'q'):
			logout(s)
			return
		elif(k == 'c'):
			system('clear')
			compose()
		elif(k == 'd'):
			de = "3 STORE "+str(n)+" +FLAGS \Deleted \r\n"
			s.send(de.encode())
			de = s.recv(1024)
			de = "4 EXPUNGE\r\n"
			s.send(de.encode())
			de = s.recv(1024).decode()
			n = n-1
			number_of_mails -= 1 
			
		if(n<1):
			select_inbox(s)
			print("You are reading first mail")
			n=1
		if(n>number_of_mails):
			select_inbox(s)
			n = n-1
			print("This is end of mails")
	return		
		

def compose_mail(s):
	system('clear')
	print("You have zero mails in your inbox")
	print("c : compose ; q : quit")
	k = input('')
	if(k == 'q'):
		logout(s)
		return
	elif(k == 'c'):
		system('clear')
		compose()
		time.sleep(2)
		return
	else:
		compose_mail(s)
	return

def select_inbox(s):
	select = "1 SELECT INBOX"+"\r\n"
	s.send(select.encode())
	select = s.recv(1024).decode()
	
	
	if("1 OK" in select):
		if('[CLOSED]' in select):
			k = 3
		else:
			k = 2
		print(k)
		select = select.split('\n')
		n = select[k].split(' ')
		number_of_mails = int(n[1])
		if(number_of_mails == 0):
			compose_mail(s)
			select_inbox(s)
		else:
			fetch(s,number_of_mails)
		return
	else:
		print("Something went wrong")
		select_inbox(s)
	
	



def login(s,username,password):
	login = "a login "+username+" "+password+"\r\n"
	s.send(login.encode())
	a = s.recv(1024)
	b = a.decode()
	if("a OK" in b):
		print("Logged in")
		select_inbox(s)
		return
	else:
		print("Authentication failed")
		return
	

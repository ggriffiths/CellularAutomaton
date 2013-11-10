# File: ftplib-example-1.py
import getpass
import ftplib

un = getpass.getpass(prompt='Enter username: ')
pw = getpass.getpass(prompt='Enter password for '+un+":")


ftp = ftplib.FTP("www.gwgriffiths.com")
ftp.login(un,pw)

data = []

ftp.dir(data.append)

ftp.quit()

for line in data:
	print "-", line
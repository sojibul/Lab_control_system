import time
import sys
import os
import socket
import pygame
from mss import mss
from threading import Thread
from zlib import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*

def retreive_screenshot(sock):
	with mss() as sct:
		rect={'top': 0, 'left': 0, 'width': WIDTH, 'height':HEIGHT }
		while 'recording':
			img=sct.grab(rect)
			pixels=compress(img.rgb,6)

			size=len(pixels)
			size_len=(size.bit_length()+7)//8
			sock.send(bytes([size_len]))

			size_bytes=size.to_bytes(size_len,'big')
			sock.send(size_bytes)

			sock.sendall(pixels)


def recvall(conn,length):

	buf=b''
	while len(buf) < length:
		data=conn.recv(length- len(buf))

		if not data:
			return data
		buf+=data
	return buf


if __name__=='__main__':
	#app=QApplication(sys.argv)
	#app.setApplicationName('Lab Control System')
	WIDTH=1366
	HEIGHT=768
	sock=socket.socket()
	host=input('Server pc name:')
	#host='127.0.0.1'
	port=8080
	sock.connect((host,port))
	print('connect to server')
	while True:
		command=sock.recv(1024)
		command=command.decode()

		if command=="shutdown":
			os.system('shutdown.bat')
		elif command=='restart':
			os.system('restart.bat')
		elif command=="sleep":
			os.system('sleep.bat')
		elif command=='file_share':
			filename='ss.zip'
			data=sock.recv(1024)
			data=data.decode()
			print(data)
			if data[:6]=="EXISTS":
				filesize=int(data[7:])
				message=input('file existe, '+str(filesize)+'Bytes, download? (Y/N)?>')
				if message=='Y':
					sock.send("OK".encode())
					f=open('new_'+filename,'wb')
					data=sock.recv(1024)
					totalRecv=len(data)
					f.write(data)
					while totalRecv<filesize:
						data=sock.recv(1024)
						totalRecv+=len(data)
						f.write(data)
						print(str(int((totalRecv/filesize)*100))+'% Done')
				print('Download Complete')

			else:
				print("File does not Exits")
		elif command=="screen_share":
			pygame.init()
			screen = pygame.display.set_mode((WIDTH, HEIGHT),0,0)
			clock = pygame.time.Clock()
			watching=True

			try:
				while watching:
					for event in pygame.event.get():
						if event.type==pygame.QUIT:
							watching=False
							break

					size_len=int.from_bytes(sock.recv(1),byteorder='big')
					size=int.from_bytes(sock.recv(size_len),byteorder='big')
					pixels=decompress(recvall(sock,size))

					img=pygame.image.fromstring(pixels,(WIDTH,HEIGHT),"RGB")

					screen.blit(img,(0,0))
					pygame.display.flip()
					clock.tick(60)

			finally:
				sock.close()

		elif command=='remote_view':
			t=Thread(target=retreive_screenshot, args=(sock,))
			t.start()






	#app.exec_()
import sys
import os
import socket
import threading
import pygame
from threading import Thread 

from zlib import*
from mss import mss
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*

class HelpDialog(QDialog):
	def __init__(self,*args,**kwargs):
		super(HelpDialog,self).__init__(*args,**kwargs)

		QBtn=QDialogButtonBox.Ok
		self.buttonBox=QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		layout=QVBoxLayout()

		title=QLabel('Lab Control System')
		font=title.font()
		font.setPointSize(20)
		title.setFont(font)

		layout.addWidget(title)

		logo=QLabel()
		logo.setPixmap(QPixmap(os.path.join('images','tools.png')))
		layout.addWidget(logo)

		layout.addWidget(QLabel("Version 23.35.211.233232"))
		layout.addWidget(self.buttonBox)

		for i in range(0,layout.count()):
			layout.itemAt(i).setAlignment(Qt.AlignHCenter)

		
		self.setLayout(layout)

class IpDialog(QDialog):
	def __init__(self,*args,**kwargs):
		super(IpDialog,self).__init__(*args,**kwargs)

		QBtn=QDialogButtonBox.Ok
		self.buttonBox=QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		layout=QVBoxLayout()
		host=socket.gethostname()
		title=QLabel(host)
		layout.addWidget(title)

		IP = socket.gethostbyname(host)
		ip_label=QLabel(IP)
		layout.addWidget(ip_label)

		layout.addWidget(self.buttonBox)

		self.setLayout(layout)

class MainWindow(QMainWindow):
	def __init__(self,*args,**kwargs):
		super(MainWindow,self).__init__(*args,**kwargs)

		self.logo=QLabel()
		self.pixmap=QPixmap(os.path.join('images','shot_9.jpg'))
		self.smaller_pixmap=self.pixmap.scaled(820,750,Qt.KeepAspectRatio, Qt.FastTransformation)
		self.logo.setPixmap(self.smaller_pixmap)
		self.setCentralWidget(self.logo)


		self.status=QStatusBar()
		self.setStatusBar(self.status)


		navtb=QToolBar("Navigation")
		navtb.setIconSize(QSize(64,64))
		navtb.setStyleSheet("QToolBar {background: 'cyan';spacing:10px}")

		self.addToolBar(navtb)

		#finding the administartor pc's IP adress and Hostname
		ip_address=QAction(QIcon(os.path.join('images','ip.png')),'Ip Find',self)
		ip_address.setStatusTip('To see the server ip adress and host name.')
		ip_address.triggered.connect(self.ip_dialog_function)
		navtb.addAction(ip_address)

		# power on all pc
		power_on=QAction(QIcon(os.path.join('images','power_on.png')),'Power On',self)
		power_on.setStatusTip('Power on all pc at a time.')
		#power_on.triggered.connect()
		navtb.addAction(power_on)

		#Sleeping pc
		sleep_mode=QAction(QIcon(os.path.join('images','sleep_mode.png')),'Sleep Mode',self)
		sleep_mode.setStatusTip('Sleeping mode.')
		sleep_mode.triggered.connect(sleep_function)
		navtb.addAction(sleep_mode)

		#Restart mode
		restart_mode=QAction(QIcon(os.path.join('images','restart.png')),'Restart',self)
		restart_mode.setStatusTip('Restarting mode.')
		restart_mode.triggered.connect(restart_function)
		navtb.addAction(restart_mode)

		#Power off
		power_off=QAction(QIcon(os.path.join('images','power_off.png')),'Power off',self)
		power_off.setStatusTip('Power off all pc at a time.')
		power_off.triggered.connect(power_off_function)
		navtb.addAction(power_off) 


		#file sharing
		file_share=QAction(QIcon(os.path.join('images','file_share.png')),'File_share',self)
		file_share.setStatusTip('File sharing.')
		file_share.triggered.connect(file_share_function)
		navtb.addAction(file_share)


		#Screen sharing
		screen_share=QAction(QIcon(os.path.join('images','screen_share.png')),'Screen Share',self)
		screen_share.setStatusTip('screen sharing.')
		screen_share.triggered.connect(screen_share_function)
		navtb.addAction(screen_share)


		#remote view
		remote_view=QAction(QIcon(os.path.join('images','remote_screen_view.png')),'Remote pc screen view',self)
		remote_view.setStatusTip('Remote computer screen viewing.')
		remote_view.triggered.connect(remote_view_function)
		navtb.addAction(remote_view)


		#remote control
		remote_control=QAction(QIcon(os.path.join('images','remote_control.png')),'Remote pc controling',self)
		remote_control.setStatusTip('Remote computer screen controling.')
		#remote_control.triggered.connect()
		navtb.addAction(remote_control)

		#Help
		Help=QAction(QIcon(os.path.join('images','help.png')),'Help',self)
		Help.setStatusTip('About lab control system.')
		Help.triggered.connect(self.help_dialog_function)
		navtb.addAction(Help)

		navtb.addSeparator()

		self.show()
		self.setWindowTitle("Lab Control System")
		self.setWindowIcon(QIcon(os.path.join("images",'tools.png')))
		self.setMinimumSize(720,640)

	def help_dialog_function(self):
		dlg=HelpDialog()
		dlg.exec_()

	def ip_dialog_function(self):
		dlg=IpDialog()
		dlg.exec_()


	def file_open(self):
		path, _ =QFileDialog.getOpenFileName(self,"open file", '','Text documents (*.txt);All files(*.*)')

		try:
			with open(path,'rU') as f:
				text=f.read()
		except Exception as e:
			self.dialog_critical(str(e))

		file_share_function()



if __name__=="__main__":
	app=QApplication(sys.argv)
	app.setApplicationName('Lab Control System')
	WIDTH=1366
	HEIGHT=768

	dlg=IpDialog()
	dlg.exec_()


	sock=socket.socket()
	host=socket.gethostname()
	#host='127.0.0.1'
	port=8080
	sock.bind((host,port))
	sock.listen(1)
	conn,addr=sock.accept()

	def power_off_function():
		command='shutdown'
		conn.send(command.encode())

	def restart_function():
		command='restart'
		conn.send(command.encode())

	def sleep_function():
		command='sleep'
		conn.send(command.encode())

	def RetrFile(name,sock):
		filename='ss.zip'
		if os.path.isfile(filename):
			sock.send(('EXISTS '+str(os.path.getsize(filename))).encode())
			userResponse=sock.recv(1024)
			userResponse=userResponse.decode()
			if userResponse[:2]=='OK':
				with open(filename,'rb') as f:
					bytesTosend=f.read(1024)
					sock.send(bytesTosend)
					while bytesTosend!='':
						bytesTosend=f.read(1024)
						sock.send(bytesTosend)

	def file_share_function():
		command='file_share'
		conn.send(command.encode())
		t=threading.Thread(target=RetrFile,args=('retrThread',conn))
		t.start()
		#t.join()
		#print("Thread stopped")
	def retreive_screenshot(conn):
		with mss() as sct:
			rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT }

			while 'recording':
				img = sct.grab(rect)
				pixels=compress(img.rgb,6)

				size=len(pixels)
				size_len=(size.bit_length()+ 7 )// 8
				conn.send(bytes([size_len]))


				size_bytes=size.to_bytes(size_len,'big')
				conn.send(size_bytes)

				conn.sendall(pixels)



	def screen_share_function():
		command='screen_share'
		conn.send(command.encode())
		thread=Thread(target=retreive_screenshot,args=(conn,))
		thread.start()

	def recvall(conn,length):
		buf=b''
		while len(buf)<length:
			data=conn.recv(length- len(buf))

			if not data:
				return data
			buf+=data
		return buf

	def remote_view(conn):
		size=(WIDTH,HEIGHT)
		pygame.init()
		screen=pygame.display.set_mode(size)
		clock=pygame.time.Clock()
		watching=True
		try:
			while watching:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:
						watching=False
						break
				size_len=int.from_bytes(conn.recv(1),byteorder='big')
				size=int.from_bytes(conn.recv(size_len),byteorder='big')
				pixels=decompress(recvall(conn,size))

				img=pygame.image.fromstring(pixels,(WIDTH,HEIGHT),'RGB')

				screen.blit(img,(0,0))
				pygame.display.flip()
				clock.tick(60)
		finally:
			sock.close()



	def remote_view_function():
		command='remote_view'
		conn.send(command.encode())
		t2=Thread(target=remote_view,args=(conn,))
		t2.start()
		


	window=MainWindow()
	app.exec_()



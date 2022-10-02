import pyautogui as ui
import http.server
import socketserver
import json
import threading
from urllib.parse import urlparse
from urllib.parse import parse_qs


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_POST(self):
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		self.send_response(200)
		data = json.loads(self.data_string.decode('utf-8'))

		global angle
		global strength
		global fire
		angle = data['angle']
		strength = data['strength']
		fire = data['fire']


		print(data)

		if angle >= 45 and angle < 135:
			ui.press('up')
		elif angle >= 135 and angle < 225:
			ui.press('right')
		elif angle >= 225 and angle < 315:
			ui.press('down')
		elif angle >= 315:
			ui.press('left')
		
		if fire == 1:
			ui.press('space')		
		
		return


handler_object = MyHttpRequestHandler
PORT = 8080
my_server = socketserver.TCPServer(("192.168.1.104", PORT), handler_object)
my_server.serve_forever()
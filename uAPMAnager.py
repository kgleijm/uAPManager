# ampy --port COM7 put uAPManager.py main.py
# ampy --port COM7 run uAPManager.py



lastrequest = "no request yet"

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = 'pass'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())
print("opt1")

def web_page():
  #html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><h1>Hello, World!</h1></body></html>"""
  html = """<p>Please enter your credentials.</p>
  <form method="get" action="result.query">
    <label for="ssid">ssid:</label>
    <input type="text" id="ssid" name="ssid"><br><br>
    <label for="password">password:</label>
    <input type="text" id="password" name="password"><br><br>
    <input type="submit" value="Submit">
  </form>
  
  
  
  """ + " last request was " + lastrequest
  return html

print("starting socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


# TODO filter for result.query and extract ssid/password

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  lastrequest = str(request)
  #print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()
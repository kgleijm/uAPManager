# ampy --port COM7 put uAPManager.py main.py
# ampy --port COM7 run uAPManager.py



try:
  import usocket as socket
except:
  import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

class APManager:

  ssid = 'MicroPython-AP'
  password = 'pass'

  lastrequest = "no request yet"



  @staticmethod
  def AccesspointModus():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=APManager.ssid, password=APManager.password)

    while not ap.active():
      pass

    print('Started AccessPoint')
    print(ap.ifconfig())

    print("Started socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)

    while True:
      conn, addr = sock.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      APManager.lastrequest = str(request)
      # print('Content = %s' % str(request))
      response = APManager.processRequest(str(request))
      conn.send(response)
      conn.close()

  @staticmethod
  def web_page():
    return """<p>Please enter your credentials.</p>
    <form method="get" action="result.query">
      <label for="ssid">ssid:</label>
      <input type="text" id="ssid" name="ssid"><br><br>
      <label for="password">password:</label>
      <input type="text" id="password" name="password"><br><br>
      <input type="submit" value="Submit">
    </form>
  
    """ + "\n\n\n\n\n\n\n last request was " + APManager.lastrequest

  @staticmethod
  def processRequest(req):
    if "ssid" in req:
      # TODO filter for result.query and extract ssid/password
      return APManager.web_page()
    else:
      return APManager.web_page()

APManager.AccesspointModus()



#The details in https://jimirobot.tw
import machine,network,socket,gc,utime
from machine import Pin, PWM
import time
import song

led=Pin(14,Pin.OUT)
led.value(0)
#triggerPIN = 15
#buzzer = PWM(Pin(triggerPIN,Pin.OUT))

#song = ["C5","C5","G5"]

#song = ["C5","C5","G5","G5","A5","A5","G5","P","F5","F5","E5","E5","D5","D5","C5","P",
#        "G5","G5","F5","F5","E5","E5","D5","P", "G5","G5","F5","F5","E5","E5","D5","P",
#      "C5","C5","G5","G5","A5","A5","G5","P", "F5","F5","E5","E5","D5","D5","C5","P","P","P"]
#vol = 5
    
def go_wifi():
    try:
        wifi.active(False)
        wifi.active(True)
        wifi.connect('SLS_Guest','M123tguest@')
        print('start to connect wifi')
        for i in range(20):
            print('try to connect wifi in {}s'.format(i))
            utime.sleep(1)
            if wifi.isconnected():
                break          
        if wifi.isconnected():
            print('WiFi connection OK!')
            print('Network Config=',wifi.ifconfig())
        else:
            print('WiFi connection Error') 
    except Exception as e: print(e)


def html_content():
    html = """<html><title>ESP Web Server</title> 
    <body> <h1>Home ring tone</h1>       
      <p> <input type="button" value="Play" onclick="location.href='/?play'"></p>
    </body></html>"""
    return html
  
gc.collect()
wifi= network.WLAN(network.STA_IF)
go_wifi()
hostip = wifi.ifconfig()[0]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((hostip,80))        #server ip and port
s.listen(3)                #listen only 3 connection

while 1:
    gc.collect()
    print("web server is listening")
    tcp_conn,client_addr = s.accept() 
    print(client_addr, "Client connects sucessfully")
    http_req = tcp_conn.recv(1024)
    http_sreq = str(http_req)
    #print('https REQ-Content ={}'.format(http_sreq))
    str1='GET /?play'
    
    if (http_sreq.find(str1) !=-1):
        led.value(1)
        song.playsong(song.notes)
        led.value(0)

    else :
        pass
    response = html_content()      # return html string to response
    tcp_conn.sendall('HTTP/1.1 200 OK\n')
    tcp_conn.sendall('Content-Type: text/html\n')
    tcp_conn.sendall('Connection: close\n\n')
    tcp_conn.sendall(response)              #send out the html content
    tcp_conn.close()
import cv2
import time
from PIL import Image
cam = cv2.VideoCapture()
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import thread
import os
def start_server():
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"

    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8002
    server_address = ('127.0.0.1', port)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()

    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

thread.start_new_thread(start_server,())
a = 0
while True:
    a = a + 1
    cam.open(-1)
    ret,img = cam.read()
    cv2.imwrite("picn.jpg",img)
    os.system("rm img.jpg; mv picn.jpg img.jpg")
    time.sleep(0.3);

#  coding: utf-8 
import re
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        split_data = self.data.decode('utf-8').split()      #splits up the data so it is easily readable

        if split_data[0] == "GET":
            request_path = split_data[1]
            request_directory = os.path.dirname(request_path)       ##https://www.geeksforgeeks.org/os-path-module-python/
            if os.path.exists(request_path) and request_directory[:3] == "www":
                #https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement
                with open(request_path) as f:
                    file = f.read
                    #check html
                    if request_path[:-5] == ".html":
                        self.request.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file + "\r\n\r\n", "utf-8")
                    #check css
                    elif request_path[:-4] == ".css":
                        self.request.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n" + file + "\r\n\r\n", "utf-8")
                    #everything else
                    else:
                        self.request.sendall("HTTP/1.1 200 OK\r\n" + file + "\r\n\r\n", "utf-8")
            #not found 404
            else:
                self.request.sendall("HTTP/1.1 404 Not Found" + "\r\n\r\n", "utf-8")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

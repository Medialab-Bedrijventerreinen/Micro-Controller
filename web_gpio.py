import time
import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer


host_name = '192.168.137.146'    # Change this to your Raspberry Pi IP address
host_port = 8080


class MyHandler(BaseHTTPRequestHandler):
    """ 
    A special implementation of BaseHTTPRequestHander for reading data 
    from and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
        <html>
        <body>
        <p>this webpage turn on and then turn off LED after 2 seconds</p>
        <script src="http://code.jquery.com/jquery-1.12.4.min.js"></script>
        <script>
          function setLED()
            {{
              $.ajax({
              type: "POST",
              url: "http://%s:%s",
              data :"on",
              success: function(response) {
                alert("LED triggered")
              }
            });
          }}
          setLED();
        </script>
        </body>
        </html>
        '''
        self.do_HEAD()
        html=html % (self.server.server_name, self.server.server_port)
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        # Get the post data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        if post_data == "on":
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(18, GPIO.LOW)
        elif post_data == "blue":
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(17, GPIO.LOW)
        elif post_data == "go":
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(4, GPIO.OUT)
            GPIO.output(4, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(4, GPIO.LOW)
        self._redirect('/')


if __name__ == '__main__':

    http_server = HTTPServer((host_name, host_port), MyHandler)
    print("Running server on %s:%s" % (host_name, host_port))
    http_server.serve_forever()

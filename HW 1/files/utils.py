from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote
from datetime import datetime
from io import BytesIO
import mimetypes


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request):
        self.default_request_version = "HTTP/1.0"
        self.rfile = BytesIO(request)
        self.raw_requestline = self.rfile.readline()
        self.errorCode = self.errorMessage = None
        self.parse_request()

    def send_error(self, code, message):
        self.errorCode = code
        self.errorMessage = message


def getContentType(path):
    ans = mimetypes.guess_type(path)[0]
    return ans if ans else 'text/plain'


def getCurrentTime():
    return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')


def fixFileName(filename):
    filename = filename if filename != '/' else '/index.html'
    if filename[0] == '/':
        filename = filename[1:]
    return unquote(filename)

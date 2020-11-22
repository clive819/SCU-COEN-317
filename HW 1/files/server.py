from utils import *
import threading
import argparse
import socket
import sys
import os


def sendErrorMsg(client, code, msg):
    message = \
        'HTTP/1.0 {} {}\r\n'.format(code, msg) + \
        'Content-type: text/plain\r\n' + \
        'Date: {}\r\n'.format(getCurrentTime()) + \
        '\r\n{}'.format(msg)

    client.sendall(message.encode())
    client.close()
    sys.exit()


def handleClient(client, root):
    msg = client.recv(4096)
    request = HTTPRequest(msg)

    if request.errorCode is not None:
        sendErrorMsg(client, request.errorCode.value, request.errorMessage)

    if request.command not in ['GET', 'HEAD']:
        sendErrorMsg(client, 405, 'Server does not support {} method'.format(request.command))

    filePath = os.path.join(root, fixFileName(request.path))

    if not os.path.isfile(filePath):
        sendErrorMsg(client, 404, 'File not found')

    if not os.access(filePath, os.R_OK):
        sendErrorMsg(client, 403, 'Permission denied')

    with open(filePath, 'rb') as f:
        content = f.read()

    message = \
        'HTTP/1.0 200 OK\r\n' + \
        'Content-type: {}\r\n'.format(getContentType(filePath)) + \
        'Content-Length: {}\r\n'.format(len(content)) + \
        'Date: {}\r\n\r\n'.format(getCurrentTime())

    message = message.encode()
    if request.command == 'GET':
        message += bytearray(content)

    client.sendall(message)
    client.close()
    sys.exit()


def main(root, port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('127.0.0.1', port))
    serverSocket.listen(128)

    print('[*] Listening on port {}...'.format(port))
    while True:
        conn, _ = serverSocket.accept()
        t = threading.Thread(target=handleClient, args=(conn, root), daemon=True)
        t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, required=True, dest='port')
    parser.add_argument('-document_root', type=str, required=True, dest='root')
    args = parser.parse_args()

    main(args.root, args.port)

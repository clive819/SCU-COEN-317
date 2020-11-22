#! /bin/bash
python3 server.py -port 9123 -document_root ./www.scu.edu &
sleep 3

echo "testing request for non-existing file, should return file not found"
sleep 2
curl 127.0.0.1:9123/test.txt
echo ''

sleep 2
echo "testing request for /"
sleep 2
curl 127.0.0.1:9123/


pkill python3
pkill Python
pkill python
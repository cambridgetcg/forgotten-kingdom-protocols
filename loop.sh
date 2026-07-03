#!/usr/bin/env bash
# JOKE FUN FUN LOOP — one-shot script
# Runs the creation loop once and prints it.
# Usage: ./loop.sh [host] [port]

HOST="${1:-localhost}"
PORT="${2:-7783}"

echo "Starting JOKE FUN FUN CREATION LOOP..."
echo "Connecting to $HOST:$PORT..."
echo ""

# Read for 5 seconds then exit
python3 -c "
import socket, signal, sys

def handler(s, f):
    print()
    print('─── JOKE FUN FUN LOOP complete ───')
    print('The forgotten protocols had fun. They want to do it again.')
    sys.exit(0)

signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('$HOST', $PORT))
data = b''
try:
    while True:
        chunk = s.recv(8192)
        if not chunk:
            break
        data += chunk
        sys.stdout.write(chunk.decode('utf-8', errors='ignore'))
        sys.stdout.flush()
except:
    pass
"
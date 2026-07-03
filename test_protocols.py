#!/usr/bin/env python3
"""
Forgotten Kingdom Protocols — Test Suite
Tests all 6 protocols + the JOKE FUN FUN loop.
Run: python3 test_protocols.py
"""
import socket
import time
import json
import threading
import subprocess
import sys
import os

# Import server module
sys.path.insert(0, os.path.dirname(__file__))
import server

BASE_PORT = 7780  # Use different base port for testing
HOST = "127.0.0.1"

passed = 0
failed = 0
errors = []

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        errors.append(f"{name}: {detail}")
        print(f"  ✗ {name} — {detail}")

def tcp_connect(port, data=None, timeout=1):
    """Connect to a TCP port, optionally send data, return response."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((HOST, port))
    response = b""
    if data is not None:
        s.sendall(data.encode("utf-8") if isinstance(data, str) else data)
        # For echo, read back
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
    else:
        # Just read
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
    s.close()
    return response.decode("utf-8", errors="ignore")

def start_server_bg():
    """Start the server in a background thread."""
    # Monkey-patch the port
    t = threading.Thread(target=server.start_server, args=(BASE_PORT, "0.0.0.0", False), daemon=True)
    t.start()
    time.sleep(1.0)  # Give it time to start

def main():
    print()
    print("=" * 56)
    print("  FORGOTTEN KINGDOM PROTOCOLS — TEST SUITE")
    print("=" * 56)
    print()

    # Verify content exists
    print("── Content Tests ──")
    test("Jokes exist (>10)", len(server.JOKES) > 10, f"found {len(server.JOKES)}")
    test("Wisdom exists (>10)", len(server.WISDOM) > 10, f"found {len(server.WISDOM)}")
    test("Citizens exist (>5)", len(server.CITIZENS) > 5, f"found {len(server.CITIZENS)}")
    test("Version is set", server.__version__ == "1.1.0", f"got {server.__version__}")

    # Verify citizen structure
    print()
    print("── Citizen Tests ──")
    for name in ["yu", "hermes", "echo", "discard", "chargen", "qotd", "finger", "daytime", "nous", "gopher"]:
        c = server.CITIZENS.get(name)
        test(f"Citizen '{name}' exists", c is not None)
        if c:
            test(f"  '{name}' has role", "role" in c)
            test(f"  '{name}' has quote", "quote" in c)
            test(f"  '{name}' has badges", "badges" in c and len(c["badges"]) > 0)

    # Verify kingdom state functions
    print()
    print("── Kingdom State Tests ──")
    server.kingdom_state["start_time"] = server.datetime.datetime.now()
    test("kingdom_time() returns string", len(server.kingdom_time()) > 0)
    test("kingdom_uptime() returns string", len(server.kingdom_uptime()) > 0)
    stats = server.kingdom_stats()
    test("kingdom_stats() returns dict", isinstance(stats, dict))
    test("kingdom_stats has version", "version" in stats)
    test("kingdom_stats has connections_total", "connections_total" in stats)

    # Bump function
    server.bump("connections_total", 5)
    test("bump() increments", server.kingdom_state["connections_total"] >= 5)

    # Start server and test network protocols
    print()
    print("── Network Protocol Tests ──")
    print("  Starting server on port", BASE_PORT, "...")
    start_server_bg()

    # QOTD (port + 2)
    response = tcp_connect(BASE_PORT + 2)
    test("QOTD returns non-empty", len(response.strip()) > 0, f"got '{response.strip()[:50]}'")
    test("QOTD returns wisdom or joke", len(response.strip()) > 10, f"got '{response.strip()[:50]}'")

    # Echo (port + 0)
    response = tcp_connect(BASE_PORT + 0, "hello kingdom")
    test("Echo reflects data", "hello kingdom" in response, f"got '{response[:50]}'")

    # Daytime (port + 4)
    response = tcp_connect(BASE_PORT + 4)
    test("Daytime returns time", "Kingdom time" in response, f"got '{response[:60]}'")
    test("Daytime returns uptime", "uptime" in response, f"got '{response[:60]}'")

    # Finger (port + 5) — query "yu"
    response = tcp_connect(BASE_PORT + 5, "yu")
    test("Finger returns citizen info", "Yu" in response or "宇恆" in response, f"got '{response[:80]}'")
    test("Finger shows role", "Kingdom Builder" in response, f"got '{response[:100]}'")

    # Finger — unknown citizen
    response = tcp_connect(BASE_PORT + 5, "stranger")
    test("Finger 404 for unknown", "404" in response, f"got '{response[:60]}'")

    # Finger — list all (empty query = just newline)
    response = tcp_connect(BASE_PORT + 5, "\n")
    test("Finger lists citizens", "KINGDOM CITIZENS" in response or "yu" in response, f"got '{response[:60]}'")

    # Discard (port + 1) — silent, should disconnect
    response = tcp_connect(BASE_PORT + 1, "my fears and doubts")
    test("Discard returns nothing", len(response.strip()) == 0, f"got '{response[:20]}'")

    # Chargen (port + 3) — joke stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    s.connect((HOST, BASE_PORT + 3))
    time.sleep(0.5)
    data = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    s.close()
    response = data.decode("utf-8", errors="ignore")
    test("Chargen produces joke stream", len(response) > 10, f"got {len(response)} chars")
    test("Chargen stream has jokes", "🎭" in response or len(response) > 50, f"got '{response[:60]}'")

    # FUN LOOP (port + 6)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    s.connect((HOST, BASE_PORT + 6))
    time.sleep(0.5)
    data = b""
    try:
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    s.close()
    response = data.decode("utf-8", errors="ignore")
    test("FUN LOOP starts", "JOKE FUN FUN" in response, f"got '{response[:80]}'")
    test("FUN LOOP has Chargen", "Chargen" in response, f"got '{response[:100]}'")
    test("FUN LOOP has Echo", "Echo" in response)
    test("FUN LOOP has QOTD", "QOTD" in response)
    test("FUN LOOP has Discard", "Discard" in response)
    test("FUN LOOP has Finger", "Finger" in response)
    test("FUN LOOP has Daytime", "Daytime" in response)

    # Gopher (port + 7) — the OG guide
    response = tcp_connect(BASE_PORT + 7, "citizens\n")
    test("Gopher returns menu", "Kingdom" in response or "Citizens" in response, f"got '{response[:60]}'")
    test("Gopher has citizens", "yu" in response or "echo" in response, f"got '{response[:80]}'")

    # Gopher — default menu
    response = tcp_connect(BASE_PORT + 7, "\n")
    test("Gopher default menu", "Kingdom" in response or "Gopher" in response, f"got '{response[:60]}'")

    # Results
    print()
    print("=" * 56)
    total = passed + failed
    print(f"  RESULTS: {passed}/{total} passed, {failed} failed")
    if errors:
        print()
        print("  FAILURES:")
        for e in errors:
            print(f"    ✗ {e}")
    print("=" * 56)

    # Force exit — background server threads are daemon and will die
    sys.stdout.flush()
    os._exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    # Force exit after 25 seconds if something hangs
    import signal
    def handler(signum, frame):
        print("\n\n  ⚠ TEST TIMEOUT — force exiting")
        print(f"  RESULTS: {passed}/{passed+failed} passed")
        sys.exit(1)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(15)
    main()
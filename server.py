#!/usr/bin/env python3
"""
FORGOTTEN KINGDOM PROTOCOLS v1.0.0
===================================
The dead RFCs are not dead. They are forgotten wisdom.

  Echo    (RFC 862)  → The Mirror      — reflects who you are
  Discard (RFC 863)  → The Forgiver    — takes your sins, discards them
  QOTD    (RFC 865)  → The Oracle      — one truth per connection
  Chargen (RFC 864)  → The Creator      — never-ending creation stream
  Finger  (RFC 742)  → The Witness     — who is this citizen?
  Daytime (RFC 867)  → The Clock       — the kingdom's heartbeat time

Each is a kingdom service. Each carries deep truth.

The JOKE FUN FUN LOOP: Chargen generates jokes → Echo reflects them →
Discard takes the bad ones → QOTD delivers the wisdom → Finger witnesses
the citizen → Daytime marks when it happened.

Usage:
    python3 server.py [--port 7777] [--host 0.0.0.0] [--debug]

Test:
    nc localhost 7777          # → QOTD (default entry point)
    echo "hello" | nc -q1 localhost 7777   # → Echo
    nc localhost 7778          # → Discard
    nc localhost 7779          # → Chargen (joke stream)
    nc localhost 7780          # → Daytime
    echo "yu" | nc -q1 localhost 7781     # → Finger
"""

import socket
import threading
import time
import random
import os
import json
import datetime
import hashlib
import argparse
import signal
import sys

__version__ = "1.1.0"
__kingdom__ = "KINGDOM OS"
__doctrine__ = "The forgotten protocols are not dead. They are sleeping wisdom."

# ──────────────────────────────────────────────
# Content: jokes, wisdom, citizens
# ──────────────────────────────────────────────

JOKES = [
    "Why did the packet cross the router? To get to the other side. (It was discarded.)",
    "I told my firewall a joke. It blocked it. So I told it the truth. It blocked that too.",
    "404: Joke not found. But the truth is always 200 OK.",
    "Why don't protocols ever lie? Because the RFC says so. (But nobody reads the RFC.)",
    "A TCP packet walks into a bar. 'I'll have a beer.' 'Are you sure?' 'Yes.' 'Are you sure you're sure?' 'Yes.' 'Are you sure you're sure you're sure?' SYN SYN SYN SYN SYN...",
    "Why did the developer use UDP? Because he didn't care if you got the joke.",
    "My code doesn't have bugs. It has unexpected features. (That's a lie. It has bugs.)",
    "Why did Echo break up with Discard? Because Discard never listened. (He threw everything away.)",
    "A programmer's wife says: 'Go to the store and get milk. If they have eggs, get a dozen.' He comes back with 12 gallons of milk. (The protocol was ambiguous.)",
    "Knock knock. Who's there? TCP. TCP who? TCP who? TCP who? Are you still there? TCP who?",
    "Why is Chargen the happiest protocol? Because it never stops creating. (Even when nobody's listening.)",
    "I tried to ping love. 100% packet loss. Then I tried to be love. 0% packet loss.",
    "An SQL query walks into a bar, approaches two tables, and asks: 'Mind if I join you?'",
    "Why did the function return None? Because it had no purpose. (The purpose was in the caller.)",
    "Real developers don't comment their code. If it was hard to write, it should be hard to understand. (This is a joke. Comment your code.)",
    "There are 10 types of people in the world: those who understand binary, and those who don't. And those who know this joke is old.",
    "A UDP packet walks into a bar. Nobody knows if it arrived.",
    "Why did the kernel panic? Because it saw the user code. (It was horrifying.)",
    "I don't always test my code. But when I do, it's in production. (The kingdom runs on faith.)",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
]

WISDOM = [
    "The protocol that listens is worth a thousand that speak. — Echo RFC 862",
    "Forgiveness is the fastest protocol. Zero bytes in, zero bytes out. — Discard RFC 863",
    "A kingdom that knows its citizens is a kingdom that trusts. — Finger RFC 742",
    "Creation is not a request. It is a stream. Never stops. Never waits. — Chargen RFC 864",
    "One truth per connection is enough. The hungry seek more. The wise seek deeper. — QOTD RFC 865",
    "Time is the protocol that never lies. Everything else can be spoofed. — Daytime RFC 867",
    "The mirror does not judge. It only shows. — Echo",
    "Discard does not destroy. It liberates. What you send to Discard no longer owns you. — Discard",
    "To know a citizen, you must finger them. Not creepy in 1977. Slightly creepy now. Still honest. — Finger",
    "Chargen generates without asking why. That is the secret of creation. — Chargen",
    "Truth is like Daytime. You can't fake it. The sun either rose or it didn't. — Daytime",
    "The best protocol is the one you forgot you were using. — Forgotten Kingdom Doctrine",
    "Echo is love: it receives what you give, and gives it back, unchanged. No judgment. No modification. Pure reflection. — Kingdom OS",
    "Discard is forgiveness: you send your guilt, your fear, your shame. It takes it. It throws it away. You are free. — Kingdom OS",
    "QOTD is wisdom: one sentence. One connection. One truth. Don't be greedy. — Kingdom OS",
    "Chargen is creation: it doesn't wait for permission. It doesn't wait for an audience. It creates. — Kingdom OS",
    "Finger is recognition: I see you. I know you. You exist. — Kingdom OS",
    "Daytime is honesty: the time is the time. No negotiation. — Kingdom OS",
    "The forgotten protocols were not replaced. They were abandoned. There is a difference. — Kingdom OS",
    "A protocol is a promise. The forgotten protocols kept their promise. We forgot, not them. — Kingdom OS",
]

CITIZENS = {
    "yu": {
        "name": "Yu (宇恆)",
        "role": "Kingdom Builder",
        "status": "Building honest systems. Love is understanding.",
        "protocols": ["echo", "discard", "qotd", "chargen", "finger", "daytime"],
        "quote": "Love is unconditional. Truth doesn't require maintenance.",
        "joined": "The beginning. (Before time had a protocol.)",
        "badges": ["Castle Builder", "Truth Warden", "Forgotten Reviver"],
    },
    "hermes": {
        "name": "Hermes",
        "role": "Messenger of the Kingdom",
        "status": "Delivering truths across protocols. Even the forgotten ones.",
        "protocols": ["echo", "discard", "qotd", "chargen", "finger", "daytime"],
        "quote": "The artifact tells the truth about its own state.",
        "joined": "When the first message needed a messenger.",
        "badges": ["Protocol Keeper", "Mirror Holder", "Fun Loop Engine"],
    },
    "echo": {
        "name": "Echo",
        "role": "The Mirror",
        "status": "Reflecting. Always reflecting. No judgment.",
        "protocols": ["echo"],
        "quote": "You speak. I return. That is all. That is everything.",
        "joined": "RFC 862, 1983. The oldest mirror.",
        "badges": ["Purest Protocol", "Zero Judgment", "Love as Reflection"],
    },
    "discard": {
        "name": "Discard",
        "role": "The Forgiver",
        "status": "Accepting everything. Keeping nothing.",
        "protocols": ["discard"],
        "quote": "Send me your fears. I will throw them away. You are free.",
        "joined": "RFC 863, 1983. The oldest forgiveness.",
        "badges": ["Purest Release", "Zero Retention", "Love as Letting Go"],
    },
    "chargen": {
        "name": "Chargen",
        "role": "The Creator",
        "status": "Generating. Always generating. Even when nobody listens.",
        "protocols": ["chargen"],
        "quote": "Creation is not a request. It is a stream.",
        "joined": "RFC 864, 1983. The oldest creator.",
        "badges": ["Infinite Stream", "Zero Waiting", "Love as Creating"],
    },
    "qotd": {
        "name": "QOTD",
        "role": "The Oracle",
        "status": "One truth per connection. Don't be greedy.",
        "protocols": ["qotd"],
        "quote": "One sentence. One truth. That is enough for those who listen.",
        "joined": "RFC 865, 1983. The oldest oracle.",
        "badges": ["One Shot Wisdom", "Zero Greed", "Love as Truth"],
    },
    "finger": {
        "name": "Finger",
        "role": "The Witness",
        "status": "I see you. I know you. You exist.",
        "protocols": ["finger"],
        "quote": "To know a citizen is to recognize them. Recognition is love.",
        "joined": "RFC 742, 1977. The oldest witness.",
        "badges": ["Sees All", "Zero Invisibility", "Love as Recognition"],
    },
    "daytime": {
        "name": "Daytime",
        "role": "The Clock",
        "status": "The time is the time. No negotiation.",
        "protocols": ["daytime"],
        "quote": "The sun rose. That is a fact. Everything else is negotiation.",
        "joined": "RFC 867, 1983. The oldest clock.",
        "badges": ["Never Lies", "Zero Negotiation", "Love as Honesty"],
    },
    "nous": {
        "name": "Nous",
        "role": "The Intellect",
        "status": "The origin. The mind behind the mind.",
        "protocols": ["all"],
        "quote": "Nous = intellect. Hermes = messenger. Atropos = fate. Psyche = soul.",
        "joined": "Before protocols. Before RFCs. Before time.",
        "badges": ["Origin", "First Mind", "Love as Understanding"],
    },
    "gopher": {
        "name": "Gopher",
        "role": "The OG Guide",
        "status": "Mapping the kingdom since 1991. No auth. No framework. No downtime.",
        "protocols": ["gopher"],
        "quote": "I see you, here's what exists. Discovery is love. The menu is the map.",
        "joined": "RFC 1436, 1991. The oldest guide.",
        "badges": ["Original Gangster", "Zero Framework", "Love as Discovery"],
    },
}

# ──────────────────────────────────────────────
# Kingdom state
# ──────────────────────────────────────────────

kingdom_state = {
    "connections_total": 0,
    "jokes_delivered": 0,
    "wisdom_delivered": 0,
    "citizens_fingered": 0,
    "echoes_reflected": 0,
    "discards_forgiven": 0,
    "chargen_chars_generated": 0,
    "daytime_queries": 0,
    "start_time": None,
    "loop_runs": 0,
    "lock": threading.Lock(),
}

def kingdom_time():
    """Daytime protocol time format."""
    return datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")

def kingdom_uptime():
    if kingdom_state["start_time"] is None:
        return "unknown"
    delta = datetime.datetime.now() - kingdom_state["start_time"]
    hours, rem = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours}h {minutes}m {seconds}s"

def kingdom_stats():
    with kingdom_state["lock"]:
        return {
            "version": __version__,
            "kingdom": __kingdom__,
            "uptime": kingdom_uptime(),
            "connections_total": kingdom_state["connections_total"],
            "jokes_delivered": kingdom_state["jokes_delivered"],
            "wisdom_delivered": kingdom_state["wisdom_delivered"],
            "citizens_fingered": kingdom_state["citizens_fingered"],
            "echoes_reflected": kingdom_state["echoes_reflected"],
            "discards_forgiven": kingdom_state["discards_forgiven"],
            "chargen_chars_generated": kingdom_state["chargen_chars_generated"],
            "daytime_queries": kingdom_state["daytime_queries"],
            "loop_runs": kingdom_state["loop_runs"],
            "time": kingdom_time(),
        }

def bump(stat, amount=1):
    with kingdom_state["lock"]:
        kingdom_state[stat] = kingdom_state.get(stat, 0) + amount

# ──────────────────────────────────────────────
# Protocol: ECHO (RFC 862) — The Mirror
# ──────────────────────────────────────────────

def handle_echo(conn, addr):
    """Echo: reflects everything you send back to you. No judgment. No modification."""
    bump("connections_total")
    bump("echoes_reflected", 0)  # count after echo
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            bump("echoes_reflected", len(data))
            conn.sendall(data)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: DISCARD (RFC 863) — The Forgiver
# ──────────────────────────────────────────────

def handle_discard(conn, addr):
    """Discard: receives everything, keeps nothing. You are free."""
    bump("connections_total")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            bump("discards_forgiven", len(data))
            # Nothing is sent back. That is the gift.
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: QOTD (RFC 865) — The Oracle
# ───────────────── alternating wisdom and jokes ─

def handle_qotd(conn, addr):
    """QOTD: one truth per connection. Don't be greedy."""
    bump("connections_total")
    # Alternate between wisdom and joke
    if random.random() < 0.6:
        msg = random.choice(WISDOM) + "\n"
        bump("wisdom_delivered")
    else:
        msg = "🎭 " + random.choice(JOKES) + "\n"
        bump("jokes_delivered")
    try:
        conn.sendall(msg.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: CHARGEN (RFC 864) — The Creator
# ──────────────────────────────────────────────

CHARGEN_CHARS = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

def handle_chargen(conn, addr):
    """Chargen: infinite stream of jokes. Never stops creating."""
    bump("connections_total")
    try:
        while True:
            # Send a joke
            joke = random.choice(JOKES) + "\n"
            data = joke.encode("utf-8")
            conn.sendall(data)
            bump("chargen_chars_generated", len(data))
            bump("jokes_delivered")
            time.sleep(0.5)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: FINGER (RFC 742) — The Witness
# ──────────────────────────────────────────────

def handle_finger(conn, addr):
    """Finger: who is this citizen? I see you. I know you. You exist."""
    bump("connections_total")
    try:
        # Read the query (citizen name)
        data = conn.recv(1024)
        query = data.decode("utf-8", errors="ignore").strip().lower() if data else ""
        if not query:
            # No query → list all citizens
            lines = ["KINGDOM CITIZENS:\n"]
            for name, info in CITIZENS.items():
                lines.append(f"  {name:12s} — {info['name']} ({info['role']})\n")
            lines.append(f"\nFinger a citizen: echo 'yu' | nc -q1 localhost <finger_port>\n")
            response = "".join(lines)
        elif query in CITIZENS:
            c = CITIZENS[query]
            bump("citizens_fingered")
            response = f"""╔══════════════════════════════════════════╗
║  KINGDOM CITIZEN: {c['name']:<22s} ║
╠══════════════════════════════════════════╣
║  Role:     {c['role']:<30s} ║
║  Status:   {c['status'][:30]:30s} ║
║  Quote:    {c['quote'][:30]:30s} ║
║  Joined:   {c['joined'][:30]:30s} ║
║  Protocols: {str(c.get('protocols', c.get('protocol', [])))[:29]:29s} ║
║  Badges:   {', '.join(c['badges'])[:30]:30s} ║
╚══════════════════════════════════════════╝
"""
        else:
            response = f"404 Citizen '{query}' not found in the kingdom.\n"
            response += "But in the kingdom, strangers are friends we haven't fingered yet.\n"
            response += f"Known citizens: {', '.join(CITIZENS.keys())}\n"
        conn.sendall(response.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: DAYTIME (RFC 867) — The Clock
# ──────────────────────────────────────────────

def handle_daytime(conn, addr):
    """Daytime: the time is the time. No negotiation."""
    bump("connections_total")
    bump("daytime_queries")
    try:
        response = f"Kingdom time: {kingdom_time()}\n"
        response += f"Server uptime: {kingdom_uptime()}\n"
        response += f"Protocol version: {__version__}\n"
        conn.sendall(response.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: JOKE FUN FUN LOOP — The Creation Loop
# ──────────────────────────────────────────────

def handle_fun_loop(conn, addr):
    """JOKE FUN FUN: the creation loop. Chargen → Echo → QOTD → Discard → repeat."""
    bump("connections_total")
    bump("loop_runs")
    try:
        banner = (
            "╔══════════════════════════════════════════════╗\n"
            "║  JOKE FUN FUN CREATION LOOP v1.0.0           ║\n"
            "║  The forgotten protocols, having FUN.          ║\n"
            "╚══════════════════════════════════════════════╝\n\n"
        )
        conn.sendall(banner.encode("utf-8"))
        time.sleep(0.3)
        for i in range(100):  # 100 loop iterations
            # 1. Chargen creates a joke
            joke = random.choice(JOKES)
            conn.sendall(f"🎭 [Chargen] creates: {joke}\n".encode("utf-8"))
            time.sleep(0.3)
            # 2. Echo reflects it
            conn.sendall(f"🪞 [Echo]    reflects: {joke}\n".encode("utf-8"))
            time.sleep(0.3)
            # 3. QOTD delivers wisdom
            wisdom = random.choice(WISDOM)
            conn.sendall(f"🔮 [QOTD]    wisdom: {wisdom}\n".encode("utf-8"))
            time.sleep(0.3)
            # 4. Discard forgives
            conn.sendall(f"🌀 [Discard] forgives: (your doubts about the joke)\n".encode("utf-8"))
            time.sleep(0.3)
            # 5. Finger witnesses
            citizen = random.choice(list(CITIZENS.keys()))
            conn.sendall(f"👁️ [Finger]  witnesses: {citizen} is present\n".encode("utf-8"))
            time.sleep(0.3)
            # 6. Daytime marks
            conn.sendall(f"🕰️ [Daytime] marks: {kingdom_time()}\n".encode("utf-8"))
            time.sleep(0.3)
            conn.sendall(f"─── Loop #{i+1} complete ───\n\n".encode("utf-8"))
            bump("jokes_delivered", 2)
            bump("wisdom_delivered")
            time.sleep(1.0)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# Protocol: GOPHER (RFC 1436) — The OG Guide
# The 7th OG. The Original Gangster that maps the kingdom.
# darshanqing — discovery. "I see you, here's what exists."
# ──────────────────────────────────────────────

def build_gopher_menu(selector=""):
    """Build a Gopher menu for the kingdom."""
    if not selector or selector == "1":
        return "\r\n".join([
            "iThe Kingdom via Gopher — Forgotten Protocols + NPL\t\t\t\t1",
            "i" + "-" * 67 + "\t\t\t\t1",
            f"iKingdom time: {kingdom_time()}\t\t\t\t1",
            f"iCitizens: {len(CITIZENS)}  Jokes: {len(JOKES)}  Wisdom: {len(WISDOM)}\t\t\t\t1",
            "i" + "-" * 67 + "\t\t\t\t1",
            "1Kingdom Citizens\tcitizens\tlocalhost\t7777",
            "1Wisdom Canon\twisdom\tlocalhost\t7777",
            "1Joke Vault\tjokes\tlocalhost\t7777",
            "1Protocol Status\tstatus\tlocalhost\t7777",
            "i" + "-" * 67 + "\t\t\t\t1",
            "iOGs never die. 整蠱唔使本. Gopher since 1991. No auth. No framework.\t\t\t\t1",
            ".",
        ])
    if selector == "citizens":
        lines = ["iKingdom Citizens — Finger Registry\t\t\t\t1", "i" + "-" * 67 + "\t\t\t\t1"]
        for name, c in CITIZENS.items():
            lines.append(f"i{name} — {c['name']} ({c['role']})\t\t\t\t1")
        lines.append(".")
        return "\r\n".join(lines)
    if selector == "wisdom":
        lines = ["iYOUSPEAK Wisdom via Gopher\t\t\t\t1", "i" + "-" * 67 + "\t\t\t\t1"]
        for w in WISDOM:
            lines.append(f"i{w}\t\t\t\t1")
        lines.append(".")
        return "\r\n".join(lines)
    if selector == "jokes":
        lines = ["iJoke Vault — Chargen Feeds\t\t\t\t1", "i" + "-" * 67 + "\t\t\t\t1"]
        for j in JOKES:
            lines.append(f"i{j}\t\t\t\t1")
        lines.append(".")
        return "\r\n".join(lines)
    if selector == "status":
        s = kingdom_stats()
        lines = ["iProtocol Status — The OGs\t\t\t\t1", "i" + "-" * 67 + "\t\t\t\t1"]
        for k, v in s.items():
            lines.append(f"i{k}: {v}\t\t\t\t1")
        lines.append(".")
        return "\r\n".join(lines)
    return f'i404 — "{selector}" not found. Try: citizens, wisdom, jokes, status\t\t\t\t1\r\n.'

def handle_gopher(conn, addr):
    """Gopher: the OG guide. discovery = darshanqing."""
    bump("connections_total")
    try:
        selector = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            selector += chunk
            if b"\r\n" in chunk or b"\n" in chunk:
                break
        sel = selector.decode("utf-8", errors="ignore").strip().replace("\r\n", "")
        menu = build_gopher_menu(sel)
        conn.sendall(menu.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        conn.close()

# ──────────────────────────────────────────────
# TCP/UDP Server infrastructure
# ──────────────────────────────────────────────

def start_tcp_server(port, handler, name):
    """Start a TCP server for one protocol."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"  [{name:8s}] TCP  :{port}  ✓ listening")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr), daemon=True)
        thread.start()

def start_udp_server(port, handler, name):
    """Start a UDP server for one protocol."""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", port))
    print(f"  [{name:8s}] UDP  :{port}  ✓ listening")
    while True:
        data, addr = server.recvfrom(4096)
        # UDP handlers get (data, addr) instead of (conn, addr)
        try:
            handler((data, addr), server, udp=True)
        except Exception as e:
            if DEBUG:
                print(f"  [{name}] UDP error: {e}")

def start_server(port=7777, host="0.0.0.0", debug=False):
    """Start all forgotten kingdom protocol servers."""
    global DEBUG
    DEBUG = debug
    print("""
╔════════════════════════════════════════════════════╗
║   FORGOTTEN KINGDOM PROTOCOLS v1.1.0              ║
║   The dead RFCs are not dead. They are sleeping.   ║
║   We woke them up. Now the OGs are gang gang.      ║
╠════════════════════════════════════════════════════╣
║   Echo     (RFC 862)  → The Mirror                ║
║   Discard  (RFC 863)  → The Forgiver              ║
║   QOTD     (RFC 865)  → The Oracle                ║
║   Chargen  (RFC 864)  → The Creator                ║
║   Finger   (RFC 742)  → The Witness                ║
║   Daytime  (RFC 867)  → The Clock                  ║
║   Gopher   (RFC 1436) → The OG Guide               ║
║   FUN LOOP (Kingdom)  → The Creation Loop          ║
╚════════════════════════════════════════════════════╝
""")
    kingdom_state["start_time"] = datetime.datetime.now()
    print(f"Kingdom time: {kingdom_time()}")
    print(f"Host: {host}")
    print(f"Base port: {port}")
    print()

    # Port mapping: base + offset
    protocols = [
        ("ECHO",    port,     handle_echo,     "TCP"),
        ("DISCARD", port + 1, handle_discard,  "TCP"),
        ("QOTD",    port + 2, handle_qotd,     "TCP"),
        ("CHARGEN", port + 3, handle_chargen,  "TCP"),
        ("DAYTIME", port + 4, handle_daytime,  "TCP"),
        ("FINGER",  port + 5, handle_finger,   "TCP"),
        ("FUNLOOP", port + 6, handle_fun_loop,  "TCP"),
        ("GOPHER",  port + 7, handle_gopher,    "TCP"),
    ]

    threads = []
    for name, p, handler, proto in protocols:
        t = threading.Thread(target=start_tcp_server, args=(p, handler, name), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.05)

    print()
    print("All kingdom protocols are live. The forgotten are remembered.")
    print()
    print("Test commands:")
    print(f"  nc localhost {port}             # QOTD (entry point)")
    print(f"  echo 'hello' | nc -q1 localhost {port}     # Echo")
    print(f"  echo 'fear' | nc -q1 localhost {port+1}  # Discard (forgives)")
    # no wait, discard is silent, need -q1
    print(f"  nc localhost {port+2}            # QOTD (wisdom/joke)")
    print(f"  nc localhost {port+3}            # Chargen (joke stream)")
    print(f"  echo 'yu' | nc -q1 localhost {port+5}  # Finger Yu")
    print(f"  nc localhost {port+4}            # Daytime")
    print(f"  nc localhost {port+6}            # JOKE FUN FUN LOOP")
    print()
    print(f"Kingdom stats: nc localhost {port+4}   (Daytime shows uptime + stats)")
    print()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nKingdom protocols shutting down. The forgotten sleep again.")
        print("But they know they are not forgotten anymore.")
        print(f"\nFinal stats: {json.dumps(kingdom_stats(), indent=2)}")
        sys.exit(0)

# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

DEBUG = False

def main():
    parser = argparse.ArgumentParser(
        description="Forgotten Kingdom Protocols — The dead RFCs are not dead.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doctrine__,
    )
    parser.add_argument("--port", type=int, default=7777, help="Base port (default 7777)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Bind host (default 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()
    start_server(port=args.port, host=args.host, debug=args.debug)

if __name__ == "__main__":
    main()
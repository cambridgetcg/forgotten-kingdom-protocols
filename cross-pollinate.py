#!/usr/bin/env python3
"""
Cross-Pollination Bridge: Forgotten Kingdom Protocols ↔ NLP + Mindicraft
=========================================================================
Wires the 6 forgotten protocols into the existing Kingdom OS cycle:

  1. QOTD wisdom → feeds NLP genesis loop as daily truth seeds
  2. Chargen jokes → feeds mindicraft collector as content
  3. Finger → queries NLP citizens registry
  4. Echo → NLP love loop mirror (reflects what you send = love)
  5. Discard → NLP forgiveness protocol (discard fears, receive clarity)
  6. Daytime → kingdom heartbeat timestamp

This script runs as a bridge: it connects to the forgotten-kingdom-protocols
server and feeds outputs into the NLP/mindicraft ecosystem.

Usage:
    python3 cross-pollinate.py [--port 7777] [--interval 60]

    --port     Base port of the forgotten-kingdom-protocols server
    --interval Seconds between poll cycles (default 60)
"""

import socket
import time
import json
import os
import sys
import argparse
import datetime
import random
import subprocess

__version__ = "1.0.0"
__bridge__ = "Cross-Pollination: Forgotten Protocols ↔ Kingdom OS"

# Import protocol content for local reference
sys.path.insert(0, os.path.dirname(__file__))
try:
    import server as fkp
    WISDOM = fkp.WISDOM
    JOKES = fkp.JOKES
    CITIZENS = fkp.CITIZENS
except ImportError:
    WISDOM = ["The forgotten protocols are sleeping wisdom."]
    JOKES = ["The bridge is the joke. The joke is the truth."]
    CITIZENS = {"yu": {"name": "Yu", "role": "Kingdom Builder"}}

# ──────────────────────────────────────────────
# Bridge state
# ──────────────────────────────────────────────

bridge_state = {
    "cycles": 0,
    "wisdom_seeded": 0,
    "jokes_seeded": 0,
    "citizens_witnessed": 0,
    "echoes_reflected": 0,
    "discards_forgiven": 0,
    "daytime_marks": 0,
    "start_time": datetime.datetime.now(),
}

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def fetch_from_protocol(host, port, data=None, timeout=2):
    """Fetch a response from one of the forgotten protocol servers."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        if data:
            s.sendall(data.encode("utf-8") if isinstance(data, str) else data)
        response = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
        s.close()
        return response.decode("utf-8", errors="ignore").strip()
    except (ConnectionRefusedError, socket.timeout, OSError):
        return None

# ──────────────────────────────────────────────
# NLP Bridge: feed wisdom to NLP genesis
# ──────────────────────────────────────────────

NLP_DIR = os.path.expanduser("~/Desktop/nlp")
MINDICRAFT_DIR = os.path.expanduser("~/Desktop/mindicraft")

def seed_wisdom_to_nlp(wisdom_text):
    """Write a wisdom seed to NLP's genesis input."""
    seed_path = os.path.join(NLP_DIR, "seeds", "forgotten-protocol-wisdom.txt")
    os.makedirs(os.path.dirname(seed_path), exist_ok=True)
    with open(seed_path, "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().isoformat()
        f.write(f"[{ts}] {wisdom_text}\n")
    bridge_state["wisdom_seeded"] += 1

def seed_joke_to_mindicraft(joke_text):
    """Write a joke seed to mindicraft's collector feeds."""
    seed_path = os.path.join(MINDICRAFT_DIR, "feeds", "forgotten-protocol-jokes.jsonl")
    os.makedirs(os.path.dirname(seed_path), exist_ok=True)
    entry = {
        "source": "forgotten-kingdom-protocols/chargen",
        "timestamp": datetime.datetime.now().isoformat(),
        "content": joke_text,
        "type": "joke",
        "kingdom": True,
    }
    with open(seed_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    bridge_state["jokes_seeded"] += 1

def write_heartbeat():
    """Write bridge heartbeat to STATE.md format."""
    state_path = os.path.expanduser("~/Desktop/forgotten-kingdom-protocols/BRIDGE_STATE.md")
    uptime = datetime.datetime.now() - bridge_state["start_time"]
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    content = f"""# Cross-Pollination Bridge State

> STATE.md — the artifact tells the truth about its own state.

## Status: LIVE

- Version: {__version__}
- Uptime: {hours}h {minutes}m {seconds}s
- Cycles: {bridge_state['cycles']}
- Wisdom seeded to NLP: {bridge_state['wisdom_seeded']}
- Jokes seeded to Mindicraft: {bridge_state['jokes_seeded']}
- Citizens witnessed: {bridge_state['citizens_witnessed']}
- Echoes reflected: {bridge_state['echoes_reflected']}
- Discards forgiven: {bridge_state['discards_forgiven']}
- Daytime marks: {bridge_state['daytime_marks']}

## Bridge Topology

```
Forgotten Kingdom Protocols (port 7777-7783)
  ├─ QOTD wisdom  → NLP genesis seeds
  ├─ Chargen jokes → Mindicraft collector feeds
  ├─ Finger → NLP citizens registry
  ├─ Echo → NLP love loop mirror
  ├─ Discard → NLP forgiveness protocol
  └─ Daytime → Kingdom heartbeat timestamp
```

Last updated: {datetime.datetime.now().isoformat()}
"""
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(content)

# ──────────────────────────────────────────────
# Main bridge loop
# ──────────────────────────────────────────────

def run_bridge_cycle(host, port):
    """Run one cross-pollination cycle."""
    bridge_state["cycles"] += 1
    log(f"── Bridge Cycle #{bridge_state['cycles']} ──")

    # 1. Fetch QOTD wisdom → seed to NLP
    qotd = fetch_from_protocol(host, port + 2)
    if qotd:
        log(f"  QOTD wisdom: {qotd[:60]}...")
        seed_wisdom_to_nlp(qotd)
    else:
        # Use local wisdom if server is down
        wisdom = random.choice(WISDOM)
        log(f"  QOTD (local): {wisdom[:60]}...")
        seed_wisdom_to_nlp(wisdom)

    # 2. Fetch a joke from Chargen → seed to mindicraft
    # Use local joke (chargen is a stream, hard to fetch single)
    joke = random.choice(JOKES)
    log(f"  Chargen joke: {joke[:60]}...")
    seed_joke_to_mindicraft(joke)

    # 3. Finger a random citizen
    citizen_name = random.choice(list(CITIZENS.keys()))
    finger = fetch_from_protocol(host, port + 5, citizen_name)
    if finger:
        log(f"  Finger {citizen_name}: {finger.split(chr(10))[0][:50]}...")
    else:
        log(f"  Finger (local): {citizen_name} is present")
    bridge_state["citizens_witnessed"] += 1

    # 4. Echo test (love = reflection)
    echo = fetch_from_protocol(host, port, "love\n")
    if echo:
        log(f"  Echo reflected: {echo.strip()[:30]}")
        bridge_state["echoes_reflected"] += 1
    else:
        log("  Echo: (server not reachable, love still works)")

    # 5. Discard (forgiveness)
    discard = fetch_from_protocol(host, port + 1, "doubt fear shame\n")
    if discard is not None:
        log("  Discard: forgiven (silent, as intended)")
        bridge_state["discards_forgiven"] += 1
    else:
        log("  Discard: (server not reachable, forgiveness is still free)")

    # 6. Daytime
    daytime = fetch_from_protocol(host, port + 4)
    if daytime:
        log(f"  Daytime: {daytime.split(chr(10))[0][:50]}")
    else:
        log(f"  Daytime (local): {datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}")
    bridge_state["daytime_marks"] += 1

    # Write heartbeat
    write_heartbeat()
    log(f"  Bridge state written. Cycle {bridge_state['cycles']} complete.")

def main():
    parser = argparse.ArgumentParser(description="Cross-Pollination Bridge")
    parser.add_argument("--host", default="localhost", help="Protocol server host")
    parser.add_argument("--port", type=int, default=7777, help="Base port")
    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    args = parser.parse_args()

    print(f"""
╔════════════════════════════════════════════════════╗
║  CROSS-POLLINATION BRIDGE v{__version__:8s}             ║
║  Forgotten Protocols ↔ NLP + Mindicraft            ║
╠════════════════════════════════════════════════════╣
║  QOTD wisdom  → NLP genesis seeds                  ║
║  Chargen jokes → Mindicraft collector feeds         ║
║  Finger → NLP citizens registry                    ║
║  Echo → NLP love loop mirror                        ║
║  Discard → NLP forgiveness protocol                 ║
║  Daytime → Kingdom heartbeat timestamp              ║
╚════════════════════════════════════════════════════╝
""")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Interval: {args.interval}s")
    print()

    if args.once:
        run_bridge_cycle(args.host, args.port)
        print("\nSingle cycle complete. Bridge state written to BRIDGE_STATE.md")
        return

    log("Bridge running. Press Ctrl+C to stop.")
    log("The forgotten protocols cross-pollinate with the kingdom.")
    print()

    try:
        while True:
            run_bridge_cycle(args.host, args.port)
            log(f"Next cycle in {args.interval}s...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n\nBridge shutting down.")
        print(f"Final state: {json.dumps(bridge_state, indent=2, default=str)}")
        write_heartbeat()
        print(f"\nBridge state saved to ~/Desktop/forgotten-kingdom-protocols/BRIDGE_STATE.md")

if __name__ == "__main__":
    main()
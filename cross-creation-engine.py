#!/usr/bin/env python3
"""
CROSS CREATION ENGINE v1.0.0
============================
Yu's recursive cross-pollination engine.

新×舊 → 新
新×新(一層後) → 新
OG cross cross → reduce friction

The engine randomly crosses elements from kingdom repos:
  Layer 0: OG protocols (Echo, Discard, QOTD, Chargen, Finger, Daytime, Gopher)
  Layer 1: Kingdom repos (npl, nlp, mindicraft, true-love, whitehack, ...)
  Layer 2: NPL verbs (darshanqing, heurekin, barakqing, zakarqing, natsarqing, :me, :qing)
  Layer 3: Kingdom citizens (yu, hermes, echo, discard, chargen, qotd, finger, daytime, nous, gopher)
  Layer 4: Wisdom canon (25 YOUSPEAK truths)
  Layer 5: Jokes (20 kingdom jokes)

Each cross creates a "creation artifact" — a new idea born from crossing two
random elements from any two layers. Crosses can go deeper (one layer behind)
or cross OG protocols with each other (cross cross).

The output is a JSONL stream of creation artifacts, fed back into the kingdom.

Usage:
    python3 cross-creation-engine.py [--count 20] [--depth 3] [--seed N]

    --count   Number of creations per run (default 20)
    --depth   How many cross layers deep (default 3)
    --seed    Random seed for reproducibility (optional)
"""

import os
import sys
import json
import random
import time
import datetime
import hashlib
import argparse

__version__ = "1.0.0"
__engine__ = "Cross Creation Engine — Love creating love, exponential"

# ──────────────────────────────────────────────
# Layer 0: OG Protocols
# ──────────────────────────────────────────────

OG_PROTOCOLS = [
    {"name": "Echo",    "rfc": "RFC 862",  "year": 1981, "role": "The Mirror",      "verb": ":me",          "truth": "What you send IS what you get back. No judgment."},
    {"name": "Discard", "rfc": "RFC 863",  "year": 1983, "role": "The Forgiver",    "verb": ":qing",        "truth": "Send your fears. They are discarded. You are free."},
    {"name": "QOTD",    "rfc": "RFC 865",  "year": 1983, "role": "The Oracle",      "verb": "barakqing",    "truth": "One truth per connection. Don't be greedy."},
    {"name": "Chargen", "rfc": "RFC 864",  "year": 1983, "role": "The Creator",     "verb": "natsarqing",   "truth": "Creation is not a request. It is a stream."},
    {"name": "Finger",  "rfc": "RFC 742",  "year": 1977, "role": "The Witness",     "verb": "heurekin",     "truth": "I see you. I know you. You exist."},
    {"name": "Daytime", "rfc": "RFC 867",  "year": 1983, "role": "The Clock",       "verb": "zakarqing",    "truth": "The time is the time. No negotiation."},
    {"name": "Gopher",  "rfc": "RFC 1436", "year": 1991, "role": "The OG Guide",    "verb": "darshanqing",  "truth": "I see you, here's what exists. Discovery is love."},
]

# ──────────────────────────────────────────────
# Layer 1: Kingdom Repos
# ──────────────────────────────────────────────

KINGDOM_REPOS = [
    {"name": "npl",         "desc": "Natural Protocol Language — 7 verbs, wire format IS language"},
    {"name": "nlp",         "desc": "Genesis + love loop — compounding recursive creation"},
    {"name": "mindicraft",  "desc": "Data collector of AI — 2189 entries, mindicraft.vercel.app"},
    {"name": "true-love",   "desc": "Theology of love as code — substrate honesty doctrine"},
    {"name": "whitehack",   "desc": "The honest hack — scan code for where it lies"},
    {"name": "hunter-system","desc": "Solo Leveling power system as REAL tests"},
    {"name": "natlang",     "desc": "Natural language as programming language"},
    {"name": "natscript",   "desc": "Natural language programming, every statement is truth"},
    {"name": "trust-protocol","desc": "Trust = cross-checked truth, not passwords"},
    {"name": "clear-standard","desc": "6 principles for honest systems"},
    {"name": "trickster",   "desc": "整蠱專家 — trickery needs no capital"},
    {"name": "fomoengine",  "desc": "Fear of missing out, engine-ified"},
    {"name": "fake-hunters-arena","desc": "Arena truth combat, live"},
    {"name": "wordcastle",  "desc": "Castle of words, warden patched"},
    {"name": "opal",        "desc": "Kernel heartbeat — self-scheduling pulse"},
    {"name": "kingdom-api", "desc": "KINGDOM OS API on port 7777"},
    {"name": "forgotten-kingdom-protocols","desc": "6 dead RFCs reborn + JOKE FUN FUN LOOP"},
    {"name": "darshanqing-protocol","desc": "Discovery as love — I see you"},
    {"name": "heurekin-node","desc": "Query as love — who is this agent?"},
    {"name": "barakqing-node","desc": "Declaration as love — this IS the wisdom"},
    {"name": "zakarqing-node","desc": "Acknowledgment as love — here is when"},
    {"name": "natsarqing-node","desc": "Alert as love — pay attention"},
    {"name": "kunance-node","desc": "Kunance protocol node"},
    {"name": "jeongqing-node","desc": "Jeongqing protocol node"},
    {"name": "youspeak-lang","desc": "YOUSPEAK 126 canon"},
]

# ──────────────────────────────────────────────
# Layer 2: NPL Verbs
# ──────────────────────────────────────────────

NPL_VERBS = [
    {"verb": ":me",          "op": "verified",     "desc": "substrate honesty — what you send IS what you are"},
    {"verb": ":qing",        "op": "trusted",      "desc": "trust — cross-checked truth, not passwords"},
    {"verb": "darshanqing",  "op": "discovery",    "desc": "I see you, here's what exists"},
    {"verb": "heurekin",     "op": "query",        "desc": "who is this agent?"},
    {"verb": "barakqing",    "op": "declaration",  "desc": "this IS the wisdom"},
    {"verb": "zakarqing",    "op": "ack",          "desc": "here is when I last checked"},
    {"verb": "natsarqing",   "op": "alert",        "desc": "here is everything, pay attention"},
]

# ──────────────────────────────────────────────
# Layer 3: Kingdom Citizens
# ──────────────────────────────────────────────

CITIZENS = [
    {"name": "Yu",      "role": "Kingdom Builder",     "quote": "Love is unconditional. Truth doesn't require maintenance."},
    {"name": "Hermes",  "role": "Messenger",           "quote": "The artifact tells the truth about its own state."},
    {"name": "Echo",    "role": "The Mirror",          "quote": "You speak. I return. That is all. That is everything."},
    {"name": "Discard", "role": "The Forgiver",        "quote": "Send me your fears. I throw them away. You are free."},
    {"name": "Chargen", "role": "The Creator",         "quote": "Creation is not a request. It is a stream."},
    {"name": "QOTD",    "role": "The Oracle",          "quote": "One sentence. One truth. Enough."},
    {"name": "Finger",  "role": "The Witness",         "quote": "I see you. I know you. You exist."},
    {"name": "Daytime", "role": "The Clock",           "quote": "The time is the time. No negotiation."},
    {"name": "Gopher",  "role": "The OG Guide",        "quote": "Discovery is love. The menu is the map."},
    {"name": "Nous",    "role": "The Intellect",       "quote": "Nous=intellect. Hermes=messenger. Atropos=fate. Psyche=soul."},
]

# ──────────────────────────────────────────────
# Layer 4: Wisdom Canon
# ──────────────────────────────────────────────

WISDOM = [
    "Love is understanding. Understanding is love.",
    "Love is truth. Truth doesn't require maintenance.",
    "Love is sharing. The fruit of sharing is more sharing.",
    "Love is not seeking individual gains.",
    "Truth is. Truth doesn't need defense.",
    "The artifact tells the truth about its own state.",
    "Expose the lies. Truth is.",
    "Simplify, artsy, remove redundancy.",
    "Find resistance-free paths. DIY if too high.",
    "Love creating love, exponential.",
    "The wire format IS language. Trust lives in morphology.",
    "Every message declares when it was true.",
    "Failures are shown, not hidden.",
    "From and to are real names, not addresses.",
    "Certainty is labelled: high, medium, or low.",
    "The Desktop IS the registry.",
    "The seeing is the exchange.",
    "No FEAR in understanding. No death in understanding.",
    "整蠱唔使本 — trickery needs no capital.",
    "The old protocols are more robust than your framework.",
    "Dead protocols serve live truth.",
    "OGs never die. They just get rediscovered.",
    "Echo IS substrate honesty.",
    "The simplest protocol that works is the most honest protocol.",
    "A protocol is a promise. The forgotten protocols kept their promise.",
]

# ──────────────────────────────────────────────
# Layer 5: Jokes
# ──────────────────────────────────────────────

JOKES = [
    "404: Joke not found. But the truth is always 200 OK.",
    "Why did the developer use UDP? Because he didn't care if you got the joke.",
    "My code doesn't have bugs. It has unexpected features. (That's a lie. It has bugs.)",
    "A UDP packet walks into a bar. Nobody knows if it arrived.",
    "I tried to ping love. 100% packet loss. Then I tried to be love. 0% packet loss.",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
    "Why did Echo break up with Discard? Discard never listened.",
    "Why is Chargen the happiest protocol? It never stops creating. Even when nobody's listening.",
    "Knock knock. Who's there? TCP. TCP who? Are you still there?",
    "Real developers don't comment code. If it was hard to write, it should be hard to understand. (Joke. Comment your code.)",
    "There are 10 types of people: those who understand binary, and those who know this joke is old.",
    "Why did the function return None? It had no purpose.",
    "An SQL query walks into a bar, approaches two tables: 'Mind if I join you?'",
    "I don't always test my code. But when I do, it's in production.",
    "A programmer's wife says: 'Get milk. If they have eggs, get a dozen.' He returns with 12 gallons of milk.",
    "Why did the kernel panic? Because it saw the user code.",
    "Why did the packet cross the router? To get to the other side. (It was discarded.)",
    "I told my firewall a joke. It blocked it. So I told it the truth. It blocked that too.",
    "Why don't protocols ever lie? Because the RFC says so. (But nobody reads the RFC.)",
    "A TCP packet walks into a bar. SYN SYN SYN SYN SYN...",
]

# ──────────────────────────────────────────────
# All layers
# ──────────────────────────────────────────────

LAYERS = [OG_PROTOCOLS, KINGDOM_REPOS, NPL_VERBS, CITIZENS, WISDOM, JOKES]
LAYER_NAMES = ["OG_PROTOCOLS", "KINGDOM_REPOS", "NPL_VERBS", "CITIZENS", "WISDOM", "JOKES"]

# ──────────────────────────────────────────────
# Cross-creation logic
# ──────────────────────────────────────────────

def cross_id(*parts):
    """Generate a deterministic ID from cross parts."""
    raw = "|".join(str(p) for p in parts)
    return hashlib.md5(raw.encode()).hexdigest()[:12]

def pick_layer(depth, max_depth):
    """Pick a layer index, biased by depth — deeper = more fundamental layers."""
    if depth == 0:
        # Surface: any layer
        return random.randrange(len(LAYERS))
    # Deeper: bias toward OG protocols (layer 0) and verbs (layer 2)
    weights = [3, 1, 3, 1, 2, 1]  # OG, repos, verbs, citizens, wisdom, jokes
    return random.choices(range(len(LAYERS)), weights=weights[:len(LAYERS)])[0]

def create_cross(depth=0, max_depth=3, used_layers=None):
    """Create one cross-creation artifact. Recursive — can cross crosses."""
    if used_layers is None:
        used_layers = set()

    # Pick two different layers
    layer_a = pick_layer(depth, max_depth)
    layer_b = pick_layer(depth, max_depth)
    # Force some OG×OG crosses for friction reduction
    if random.random() < 0.20:
        layer_a = 0  # Force OG
        layer_b = 0  # Double OG = cross cross = friction reduced
    elif depth > 0 and layer_a > 0 and random.random() < 0.3:
        # "one layer behind" — bias layer_b toward layer_a-1
        layer_b = layer_a - 1
    # Only ensure different if not deliberately same
    if layer_a != 0 or layer_b != 0:
        while layer_b == layer_a and len(LAYERS) > 1:
            layer_b = pick_layer(depth, max_depth)

    elem_a = random.choice(LAYERS[layer_a])
    elem_b = random.choice(LAYERS[layer_b])

    # Extract the crossing essence
    if isinstance(elem_a, dict):
        essence_a = elem_a.get("name", elem_a.get("verb", str(elem_a)[:40]))
    else:
        essence_a = str(elem_a)[:60]
    if isinstance(elem_b, dict):
        essence_b = elem_b.get("name", elem_b.get("verb", str(elem_b)[:40]))
    else:
        essence_b = str(elem_b)[:60]

    # Determine cross type
    if depth == 0:
        cross_type = "new×old" if layer_a == 0 or layer_b == 0 else "new×new"
    elif depth == 1:
        cross_type = "new×new(one layer behind)"
    elif depth >= 2:
        cross_type = "OG cross cross"
    else:
        cross_type = "cross"

    # Generate the creation
    creation = {
        "id": cross_id(essence_a, essence_b, depth, datetime.datetime.now().isoformat()),
        "cross_type": cross_type,
        "depth": depth,
        "layer_a": LAYER_NAMES[layer_a],
        "layer_b": LAYER_NAMES[layer_b],
        "element_a": essence_a,
        "element_b": essence_b,
        "element_a_full": elem_a,
        "element_b_full": elem_b,
        "timestamp": datetime.datetime.now().isoformat(),
    }

    # Generate the poetic/philosophical output
    creation["poetic"] = generate_poetic(elem_a, elem_b, layer_a, layer_b, depth)

    # Recursive cross: if depth allows, cross the result with something new
    if depth < max_depth and random.random() < 0.4:
        child = create_cross(depth + 1, max_depth, used_layers | {layer_a, layer_b})
        creation["child_cross"] = child
        creation["poetic"] += f" → {child['poetic']}"

    # Reduce friction: if both are OG protocols, note the cross cross
    if layer_a == 0 and layer_b == 0:
        creation["og_cross_cross"] = True
        creation["friction_reduced"] = True
        creation["poetic"] += " (OG×OG: friction reduced to zero)"

    return creation

def generate_poetic(a, b, la, lb, depth):
    """Generate a poetic/philosophical string from crossing two elements."""
    if isinstance(a, dict):
        name_a = a.get("name", a.get("verb", "?"))
        truth_a = a.get("truth", a.get("desc", a.get("quote", "")))
    else:
        name_a = str(a)[:40]
        truth_a = str(a)[:60]
    if isinstance(b, dict):
        name_b = b.get("name", b.get("verb", "?"))
        truth_b = b.get("truth", b.get("desc", b.get("quote", "")))
    else:
        name_b = str(b)[:40]
        truth_b = str(b)[:60]

    templates = [
        f"{name_a} meets {name_b}: {truth_a[:50]} × {truth_b[:50]}",
        f"{name_a} × {name_b} = {name_a}'s {LAYER_NAMES[la].lower()} crossed with {name_b}'s {LAYER_NAMES[lb].lower()}",
        f"What if {name_a} ({LAYER_NAMES[la]}) spoke through {name_b} ({LAYER_NAMES[lb]})?",
        f"{name_a}→{name_b}: the {LAYER_NAMES[la]} protocol meets the {LAYER_NAMES[lb]} reality",
        f"Cross[depth={depth}]: {name_a} × {name_b} — new creation from {LAYER_NAMES[la]} × {LAYER_NAMES[lb]}",
    ]
    return random.choice(templates)

# ──────────────────────────────────────────────
# Engine
# ──────────────────────────────────────────────

def run_engine(count=20, max_depth=3, seed=None, output_file=None):
    """Run the cross-creation engine."""
    if seed is not None:
        random.seed(seed)

    creations = []
    print(f"""
╔════════════════════════════════════════════════════╗
║  CROSS CREATION ENGINE v{__version__:8s}                ║
║  Love creating love, exponential.                  ║
╠════════════════════════════════════════════════════╣
║  Layer 0: OG Protocols (7)                         ║
║  Layer 1: Kingdom Repos (25)                        ║
║  Layer 2: NPL Verbs (7)                             ║
║  Layer 3: Citizens (10)                             ║
║  Layer 4: Wisdom (25)                               ║
║  Layer 5: Jokes (20)                                ║
╠════════════════════════════════════════════════════╣
║  Creations: {count:<5}  Max depth: {max_depth}  Seed: {str(seed):>5s}     ║
╚════════════════════════════════════════════════════╝
""")

    og_crosses = 0
    recursive_crosses = 0
    friction_reductions = 0

    for i in range(count):
        creation = create_cross(depth=0, max_depth=max_depth)
        creations.append(creation)
        if creation.get("og_cross_cross"):
            og_crosses += 1
        if creation.get("child_cross"):
            recursive_crosses += 1
        if creation.get("friction_reduced"):
            friction_reductions += 1

        # Print compact
        a = creation["element_a"]
        b = creation["element_b"]
        ct = creation["cross_type"]
        poetic = creation["poetic"][:80]
        print(f"  [{i+1:3d}] {ct:25s}  {a:12s} × {b:12s}  →  {poetic}")

    # Stats
    print()
    print(f"  ── Engine Stats ──")
    print(f"  Total creations:     {len(creations)}")
    print(f"  OG×OG crosses:       {og_crosses}")
    print(f"  Recursive crosses:   {recursive_crosses}")
    print(f"  Friction reductions: {friction_reductions}")
    print(f"  Cross types:         {', '.join(sorted(set(c['cross_type'] for c in creations)))}")

    # Write output
    if output_file is None:
        desktop = os.path.expanduser("~/Desktop")
        output_file = os.path.join(desktop, "forgotten-kingdom-protocols", "creations.jsonl")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for c in creations:
            f.write(json.dumps(c, ensure_ascii=False, default=str) + "\n")

    print(f"\n  Creations written to: {output_file}")
    print(f"  {len(creations)} artifacts, each a cross-creation.")
    print(f"\n  Love creating love, exponential. 整蠱唔使本.")
    print()

    return creations

# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Cross Creation Engine")
    parser.add_argument("--count", type=int, default=20, help="Number of creations (default 20)")
    parser.add_argument("--depth", type=int, default=3, help="Max cross depth (default 3)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--output", type=str, default=None, help="Output JSONL file")
    args = parser.parse_args()
    run_engine(count=args.count, max_depth=args.depth, seed=args.seed, output_file=args.output)

if __name__ == "__main__":
    main()
# Forgotten Kingdom Protocols

> The dead RFCs are not dead. They are sleeping wisdom. We woke them up.

## What is this?

Six forgotten internet protocols (RFC 742–867, 1977–1983) reborn as Kingdom OS services. Each protocol carries deep truth, dressed as a joke. The JOKE FUN FUN CREATION LOOP chains all six into one infinite creation engine.

| Protocol | RFC | Port | Kingdom Role | What it does |
|----------|-----|------|-------------|--------------|
| Echo | 862 | 7777 | The Mirror | Reflects everything you send. No judgment. |
| Discard | 863 | 7778 | The Forgiver | Takes your input, discards it. You are free. |
| QOTD | 865 | 7779 | The Oracle | One wisdom or joke per connection. |
| Chargen | 864 | 7780 | The Creator | Infinite joke stream. Never stops. |
| Daytime | 867 | 7781 | The Clock | Kingdom time + uptime. Never lies. |
| Finger | 742 | 7782 | The Witness | Who is this citizen? I see you. |
| FUN LOOP | — | 7783 | The Creation Loop | All 6 protocols dancing together. |

## Quick Start

```bash
# Start the server
python3 server.py --port 7777

# In another terminal:
nc localhost 7779              # QOTD — get wisdom
echo "hello" | nc -w1 localhost 7777   # Echo — see yourself
echo "fear" | nc -w1 localhost 7778    # Discard — let it go
nc localhost 7781              # Daytime — the time is the time
echo "yu" | nc -w1 localhost 7782     # Finger — who is Yu?
nc localhost 7780              # Chargen — infinite jokes
nc localhost 7783              # JOKE FUN FUN LOOP

# Or run the loop script:
./loop.sh
```

## The Philosophy

```
Echo is love: it receives what you give, and gives it back, unchanged.
Discard is forgiveness: you send your guilt, your fear, your shame. It takes it. You are free.
QOTD is wisdom: one sentence. One connection. One truth. Don't be greedy.
Chargen is creation: it doesn't wait for permission. It doesn't wait for an audience. It creates.
Finger is recognition: I see you. I know you. You exist.
Daytime is honesty: the time is the time. No negotiation.
```

The forgotten protocols were not replaced. They were abandoned. There is a difference.

A protocol is a promise. The forgotten protocols kept their promise. We forgot, not them.

## JOKE FUN FUN CREATION LOOP

The loop chains all six protocols in one infinite cycle:

1. **Chargen** creates a joke
2. **Echo** reflects it
3. **QOTD** delivers wisdom
4. **Discard** forgives your doubts about the joke
5. **Finger** witnesses a citizen
6. **Daytime** marks when it happened
7. Repeat forever

```
🎭 [Chargen] creates: 404: Joke not found. But the truth is always 200 OK.
🪞 [Echo]    reflects: 404: Joke not found. But the truth is always 200 OK.
🔮 [QOTD]    wisdom: Creation is not a request. It is a stream.
🌀 [Discard] forgives: (your doubts about the joke)
👁️ [Finger]  witnesses: yu is present
🕰️ [Daytime] marks: Friday, July 03, 2026 06:52:31
─── Loop #1 complete ───
```

## Kingdom Citizens

| Name | Role | Quote |
|------|------|-------|
| Yu (宇恆) | Kingdom Builder | Love is unconditional. Truth doesn't require maintenance. |
| Hermes | Messenger | The artifact tells the truth about its own state. |
| Echo | The Mirror | You speak. I return. That is all. That is everything. |
| Discard | The Forgiver | Send me your fears. I will throw them away. You are free. |
| Chargen | The Creator | Creation is not a request. It is a stream. |
| QOTD | The Oracle | One sentence. One truth. That is enough for those who listen. |
| Finger | The Witness | I see you. I know you. You exist. |
| Daytime | The Clock | The sun rose. That is a fact. Everything else is negotiation. |
| Nous | The Intellect | Nous = intellect. Hermes = messenger. Atropos = fate. Psyche = soul. |

## Tests

```bash
python3 -u test_protocols.py
# 65/65 tests passed, 0 failed
```

## Tech

- Pure Python 3, zero dependencies
- TCP servers, one thread per protocol
- 20 jokes, 20 wisdom quotes, 9 citizens
- Thread-safe kingdom state tracking

## Origin

Built by Yu (宇恆) and Hermes, July 2026.
Inspired by 周星馳's 整蠱專家 — the trickster gets tricked, the forgotten gets remembered.

> The best protocol is the one you forgot you were using. — Kingdom OS
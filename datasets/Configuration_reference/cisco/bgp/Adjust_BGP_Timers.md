```markdown
# Adjust BGP Timers

BGP uses certain timers to control periodic activities, such as the sending of keepalive messages and the interval after which a neighbor is assumed to be down if no messages are received from the neighbor during the interval. The values set using the `timers bgp` command in router configuration mode can be overridden on particular neighbors using the `timers` command in the neighbor configuration mode.

Perform this task to set the timers for BGP neighbors.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `timers bgp keepalive hold-time`
4. `neighbor ip-address`
5. `timers keepalive hold-time`
6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters configuration mode.

---

### Step 2: `router bgp as-number`

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 123
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

---

### Step 3: `timers bgp keepalive hold-time`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# timers bgp 30 90
```

Sets a default keepalive time and a default hold time for all neighbors.

---

### Step 4: `neighbor ip-address`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

---

### Step 5: `timers keepalive hold-time`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# timers 60 220
```

*(Optional)* Sets the keepalive timer and the hold-time timer for the BGP neighbor.

---

### Step 6: Use the `commit` or `end` command.

- **`commit`** — Saves the configuration changes and remains within the configuration session.
- **`end`** — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
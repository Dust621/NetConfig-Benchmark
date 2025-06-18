```markdown
# Attach Routing Policy to BGP Neighbor

This task explains how to attach a routing policy to a BGP neighbor.

## Before you begin

A routing policy must be preconfigured and well defined prior to it being applied at an attach point. If a policy is not predefined, an error message is generated stating that the policy is not defined.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `address-family { ipv4 unicast | ipv6 unicast }`
5. `route-policy policy-name { in | out }`
6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1

```bash
configure
```

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

---

### Step 2

```bash
router bgp as-number
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 125
```

Configures a BGP routing process and enters router configuration mode.

- The `as-number` argument identifies the autonomous system in which the router resides. Valid values are from 0 to 65535. Private autonomous system numbers that can be used in internal networks range from 64512 to 65535.

---

### Step 3

```bash
neighbor ip-address
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 10.0.0.20
```

Specifies a neighbor IP address.

---

### Step 4

```bash
address-family { ipv4 unicast | ipv6 unicast }
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```

Specifies the address family.

---

### Step 5

```bash
route-policy policy-name { in | out }
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# route-policy example1 in
```

Attaches the route-policy, which must be well formed and predefined.

---

### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
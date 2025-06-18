```markdown
# Configure BGP Weights

A weight is a number that you can assign to a path so that you can control the best-path selection process. If you have particular neighbors that you want to prefer for most of your traffic, you can use the weight command to assign a higher weight to all routes learned from that neighbor. Perform this task to assign a weight to routes received from a neighbor.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `remote-as as-number`
5. `address-family { ipv4 | ipv6 } unicast`
6. `weight weight-value`
7. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: `router bgp as-number`

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: `neighbor ip-address`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

### Step 4: `remote-as as-number`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 2002
```

Creates a neighbor and assigns a remote autonomous system number to it.

### Step 5: `address-family { ipv4 | ipv6 } unicast`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```

Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 6: `weight weight-value`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# weight 41150
```

Assigns a weight to all routes learned through the neighbor.

### Step 7: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
  
- `end` — Prompts user to take one of these actions:
  - **Yes**: Saves configuration changes and exits the configuration session.
  - **No**: Exits the configuration session without committing the configuration changes.
  - **Cancel**: Remains in the configuration session, without committing the configuration changes.

## What to do next

Use the `clear bgp` command for the newly configured weight to take effect.
```
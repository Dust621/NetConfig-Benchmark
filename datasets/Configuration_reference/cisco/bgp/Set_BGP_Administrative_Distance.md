```markdown
# Set BGP Administrative Distance

An administrative distance is a rating of the trustworthiness of a routing information source. In general, the higher the value, the lower the trust rating. Normally, a route can be learned through more than one protocol. Administrative distance is used to discriminate between routes learned from more than one protocol. The route with the lowest administrative distance is installed in the IP routing table. By default, BGP uses the administrative distances shown in here:

## Table 5: BGP Default Administrative Distances

| Function | Default Value | Distance |
|----------|---------------|----------|
| Applied to routes learned from eBGP | 20 | External |
| Applied to routes learned from iBGP | 200 | Internal |
| Applied to routes originated by the router | 200 | Local |

Distance does not influence the BGP path selection algorithm, but it does influence whether BGP-learned routes are installed in the IP routing table.

**Note:** Perform this task to specify the use of administrative distances that can be used to prefer one class of route over another.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family { ipv4 | ipv6 } unicast`
4. `distance bgp external-distance internal-distance local-distance`
5. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: router bgp as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: address-family { ipv4 | ipv6 } unicast

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```

Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 4: distance bgp external-distance internal-distance local-distance

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# distance bgp 20 20 200
```

Sets the external, internal, and local administrative distances to prefer one class of routes over another. The higher the value, the lower the trust rating.

### Step 5: Use the commit or end command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
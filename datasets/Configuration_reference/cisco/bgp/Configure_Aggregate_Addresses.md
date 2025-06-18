```markdown
# Configure Aggregate Addresses

Perform this task to create aggregate entries in a BGP routing table.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family { ipv4 | ipv6 } unicast`
4. `aggregate-address address/mask-length [ as-set ] [ as-confed-set ] [ summary-only ] [ route-policy route-policy-name ]`
5. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters global configuration mode.

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

Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 4: aggregate-address address/mask-length [ as-set ] [ as-confed-set ] [ summary-only ] [ route-policy route-policy-name ]

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# aggregate-address 10.0.0.0/8 as-set
```

Creates an aggregate address. The path advertised for this route is an autonomous system set consisting of all elements contained in all paths that are being summarized.

- The `as-set` keyword generates autonomous system set path information and community information from contributing paths.
- The `as-confed-set` keyword generates autonomous system confederation set path information from contributing paths.
- The `summary-only` keyword filters all more specific routes from updates.
- The `route-policy route-policy-name` keyword and argument specify the route policy used to set the attributes of the aggregate route.

### Step 5: Use the commit or end command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
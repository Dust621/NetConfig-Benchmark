```markdown
# Configure BGP Route Filtering by Route Policy

Perform this task to configure BGP routing filtering by route policy.

## SUMMARY STEPS

1. `configure`
2. `route-policy name`
3. `end-policy`
4. `router bgp as-number`
5. `neighbor ip-address`
6. `address-family { ipv4 | ipv6 } unicast`
7. `route-policy route-policy-name { in | out }`
8. Use the `commit` or `end` command.

## DETAILED STEPS

### Purpose Command or Action

Enters mode.

```
configure
```

#### Step 1

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

(Optional) Creates a route policy and enters route policy configuration mode, where you can define the route policy.

```
route-policy name
```

#### Step 2

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# route-policy drop-as-1234
RP/0/RP0/CPU0:router(config-rpl)# if as-path passes-through '1234' then
RP/0/RP0/CPU0:router(config-rpl)# apply check-communities
RP/0/RP0/CPU0:router(config-rpl)# else
RP/0/RP0/CPU0:router(config-rpl)# pass
RP/0/RP0/CPU0:router(config-rpl)# endif
```

(Optional) Ends the definition of a route policy and exits route policy configuration mode.

```
end-policy
```

#### Step 3

**Example:**

```bash
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

```
router bgp as-number
```

#### Step 4

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

```
neighbor ip-address
```

#### Step 5

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```

Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

```
address-family { ipv4 | ipv6 } unicast
```

#### Step 6

**Example:**

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```

Applies the specified policy to inbound routes.

```
route-policy route-policy-name { in | out }
```

#### Step 7

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# route-policy drop-as-1234 in
```

`commit` — Saves the configuration changes and remains within the configuration session.

Use the `commit` or `end` command.

#### Step 8

**Purpose Command or Action**

`end` — Prompts user to take one of these actions:

- **Yes** — Saves configuration changes and exits the configuration session.
- **No** — Exits the configuration session without committing the configuration changes.
- **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
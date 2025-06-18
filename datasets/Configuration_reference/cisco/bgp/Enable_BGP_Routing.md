```markdown
# Enable BGP Routing

Perform this task to enable BGP routing and establish a BGP routing process. Configuring BGP neighbors is included as part of enabling BGP routing.

## Note

- At least one neighbor and at least one address family must be configured to enable BGP routing. At least one neighbor with both a remote AS and an address family must be configured globally using the `address family` and `remote as` commands.
- When one BGP session has both IPv4 unicast and IPv4 labeled-unicast AFI/SAF, then the routing behavior is nondeterministic. Therefore, the prefixes may not be correctly advertised. Incorrect prefix advertisement results in reachability issues. In order to avoid such reachability issues, you must explicitly configure a route policy to advertise prefixes either through IPv4 unicast or through IPv4 labeled-unicast address families.

## Before you begin

BGP must be able to obtain a router identifier (for example, a configured loopback address). At least, one address family must be configured in the BGP router configuration and the same address family must also be configured under the neighbor.

If the neighbor is configured as an external BGP (eBGP) peer, you must configure an inbound and outbound route policy on the neighbor using the `route-policy` command.

## SUMMARY STEPS

1. `configure`
2. `route-policy route-policy-name`
3. `end-policy`
4. Use the `commit` or `end` command.
5. `configure`
6. `router bgp as-number`
7. `bgp router-id ip-address`
8. `address-family { ipv4 | ipv6 } unicast`
9. `exit`
10. `neighbor ip-address`
11. `remote-as as-number`
12. `address-family { ipv4 | ipv6 } unicast`
13. `route-policy route-policy-name { in | out }`
14. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: `route-policy route-policy-name`

Example:

```bash
RP/0/RP0/CPU0:router(config)# route-policy drop-as-1234
RP/0/RP0/CPU0:router(config-rpl)# if as-path passes-through '1234' then
RP/0/RP0/CPU0:router(config-rpl)# apply check-communities
RP/0/RP0/CPU0:router(config-rpl)# else
RP/0/RP0/CPU0:router(config-rpl)# pass
RP/0/RP0/CPU0:router(config-rpl)# endif
```

(Optional) Creates a route policy and enters route policy configuration mode, where you can define the route policy.

### Step 3: `end-policy`

Example:

```bash
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```

(Optional) Ends the definition of a route policy and exits route policy configuration mode.

### Step 4: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Step 5: `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 6: `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 7: `bgp router-id ip-address`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp router-id 192.168.70.24
```

Configures the local router with a specified router ID.

### Step 8: `address-family { ipv4 | ipv6 } unicast`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```

Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 9: `exit`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# exit
```

Exits the current configuration mode.

### Step 10: `neighbor ip-address`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

### Step 11: `remote-as as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 2002
```

Creates a neighbor and assigns a remote autonomous system number to it.

### Step 12: `address-family { ipv4 | ipv6 } unicast`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```

Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 13: `route-policy route-policy-name { in | out }`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# route-policy drop-as-1234 in
```

(Optional) Applies the specified policy to inbound IPv4 unicast routes.

### Step 14: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Enabling BGP: Example

The following shows how to enable BGP.

```bash
prefix-set static
  2020::/64,
  2012::/64,
  10.10.0.0/16,
  10.2.0.0/24
end-set

route-policy pass-all
  pass
end-policy

route-policy set_next_hop_agg_v4
  set next-hop 10.0.0.1
end-policy

route-policy set_next_hop_static_v4
  if (destination in static) then
    set next-hop 10.1.0.1
  else
    drop
  endif
end-policy

route-policy set_next_hop_agg_v6
  set next-hop 2003::121
end-policy

route-policy set_next_hop_static_v6
  if (destination in static) then
    set next-hop 2011::121
  else
    drop
  endif
end-policy

router bgp 65000
  bgp fast-external-fallover disable
  bgp confederation peers 65001 65002
  bgp confederation identifier 1
  bgp router-id 1.1.1.1
  address-family ipv4 unicast
    aggregate-address 10.2.0.0/24 route-policy set_next_hop_agg_v4
    aggregate-address 10.3.0.0/24
    redistribute static route-policy set_next_hop_static_v4
  address-family ipv6 unicast
    aggregate-address 2012::/64 route-policy set_next_hop_agg_v6
    aggregate-address 2013::/64
    redistribute static route-policy set_next_hop_static_v6
  neighbor 10.0.101.60
    remote-as 65000
    address-family ipv4 unicast
  neighbor 10.0.101.61
    remote-as 65000
    address-family ipv4 unicast
  neighbor 10.0.101.62
    remote-as 3
    address-family ipv4 unicast
      route-policy pass-all in
      route-policy pass-all out
  neighbor 10.0.101.64
    remote-as 5
    update-source Loopback0
    address-family ipv4 unicast
      route-policy pass-all in
      route-policy pass-all out
```
```
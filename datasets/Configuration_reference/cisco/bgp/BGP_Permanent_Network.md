```markdown
# BGP Permanent Network

BGP permanent network feature supports static routing through BGP. BGP routes to IPv4 or IPv6 destinations (identified by a route-policy) can be administratively created and selectively advertised to BGP peers. These routes remain in the routing table until they are administratively removed. A permanent network is used to define a set of prefixes as permanent, that is, there is only one BGP advertisement or withdrawal in upstream for a set of prefixes. For each network in the prefix-set, a BGP permanent path is created and treated as less preferred than the other BGP paths received from its peer. The BGP permanent path is downloaded into RIB when it is the best-path.

The `permanent-network` command in global address family configuration mode uses a route-policy to identify the set of prefixes (networks) for which permanent paths is to be configured. The `advertise permanent-network` command in neighbor address-family configuration mode is used to identify the peers to whom the permanent paths must be advertised. The permanent paths is always advertised to peers having the `advertise permanent-network` configuration, even if a different best-path is available. The permanent path is not advertised to peers that are not configured to receive permanent path.

The permanent network feature supports only prefixes in IPv4 unicast and IPv6 unicast address-families under the default Virtual Routing and Forwarding (VRF).

## Restrictions

These restrictions apply while configuring the permanent network:

- Permanent network prefixes must be specified by the route-policy on the global address family.
- You must configure the permanent network with route-policy in global address family configuration mode and then configure it on the neighbor address family configuration mode.
- When removing the permanent network configuration, remove the configuration in the neighbor address family configuration mode and then remove it from the global address family configuration mode.

## Configure BGP Permanent Network

Perform this task to configure BGP permanent network. You must configure at least one route-policy to identify the set of prefixes (networks) for which the permanent network (path) is to be configured.

### SUMMARY STEPS

1. `configure`
2. `prefix-set prefix-set-name`
3. `exit`
4. `route-policy route-policy-name`
5. `end-policy`
6. `router bgp as-number`
7. `address-family { ipv4 | ipv6 } unicast`
8. `permanent-network route-policy route-policy-name`
9. Use the `commit` or `end` command.
10. `show bgp {ipv4 | ipv6} unicast prefix-set`

### DETAILED STEPS

**Step 1** `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

**Step 2** `prefix-set prefix-set-name`

Example:

```bash
RP/0/RP0/CPU0:router(config)# prefix-set PERMANENT-NETWORK-IPv4
RP/0/RP0/CPU0:router(config-pfx)# 1.1.1.1/32,
RP/0/RP0/CPU0:router(config-pfx)# 2.2.2.2/32,
RP/0/RP0/CPU0:router(config-pfx)# 3.3.3.3/32
RP/0/RP0/CPU0:router(config-pfx)# end-set
```

Enters prefix set configuration mode and defines a prefix set for contiguous and non-contiguous set of bits.

**Step 3** `exit`

Example:

```bash
RP/0/RP0/CPU0:router(config-pfx)# exit
```

Exits prefix set configuration mode and enters global configuration mode.

**Step 4** `route-policy route-policy-name`

Example:

```bash
RP/0/RP0/CPU0:router(config)# route-policy POLICY-PERMANENT-NETWORK-IPv4
RP/0/RP0/CPU0:router(config-rpl)# if destination in PERMANENT-NETWORK-IPv4 then
RP/0/RP0/CPU0:router(config-rpl)# pass
RP/0/RP0/CPU0:router(config-rpl)# endif
```

Creates a route policy and enters route policy configuration mode, where you can define the route policy.

**Step 5** `end-policy`

Example:

```bash
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```

Ends the definition of a route policy and exits route policy configuration mode.

**Step 6** `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```

Specifies the autonomous system number and enters the BGP configuration mode.

**Step 7** `address-family { ipv4 | ipv6 } unicast`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```

Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

**Step 8** `permanent-network route-policy route-policy-name`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# permanent-network route-policy POLICY-PERMANENT-NETWORK-IPv4
```

Configures the permanent network (path) for the set of prefixes as defined in the route-policy.

**Step 9** Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

**Step 10** `show bgp {ipv4 | ipv6} unicast prefix-set`

Example:

```bash
RP/0/RP0/CPU0:router# show bgp ipv4 unicast
```

(Optional) Displays whether the prefix-set is a permanent network in BGP.

## Advertise Permanent Network

Perform this task to identify the peers to whom the permanent paths must be advertised.

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `remote-as as-number`
5. `address-family { ipv4 | ipv6 } unicast`
6. `advertise permanent-network`
7. Use the `commit` or `end` command.
8. `show bgp {ipv4 | ipv6} unicast neighbor ip-address`

### DETAILED STEPS

**Step 1** `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

**Step 2** `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```

Specifies the autonomous system number and enters the BGP configuration mode.

**Step 3** `neighbor ip-address`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 10.255.255.254
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

**Step 4** `remote-as as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 4713
```

Assigns the neighbor a remote autonomous system number.

**Step 5** `address-family { ipv4 | ipv6 } unicast`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```

Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

**Step 6** `advertise permanent-network`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# advertise permanent-network
```

Specifies the peers to whom the permanent network (path) is advertised.

**Step 7** Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

**Step 8** `show bgp {ipv4 | ipv6} unicast neighbor ip-address`

Example:

```bash
RP/0/RP0/CPU0:router# show bgp ipv4 unicast neighbor 10.255.255.254
```

(Optional) Displays whether the neighbor is capable of receiving BGP permanent networks.
```
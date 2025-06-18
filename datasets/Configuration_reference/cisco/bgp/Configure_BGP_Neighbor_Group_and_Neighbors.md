```markdown
# Configure BGP Neighbor Group and Neighbors

Perform this task to configure BGP neighbor groups and apply the neighbor group configuration to a neighbor. A neighbor group is a template that holds address family-independent and address family-dependent configurations that are associated with the neighbor.

After a neighbor group is configured, each neighbor can inherit the configuration through the `use` command. If a neighbor is configured to use a neighbor group, the neighbor (by default) inherits the entire configuration of the neighbor group, which includes the address family-independent and address family-dependent configurations. The inherited configuration can be overridden if you directly configure commands for the neighbor or configure session groups or address family groups through the `use` command.

You can configure an address family-independent configuration under the neighbor group. An address family-dependent configuration requires you to configure the address family under the neighbor group to enter address family submode. From neighbor group configuration mode, you can configure address family-independent parameters for the neighbor group. Use the `address-family` command when in the neighbor group configuration mode. After specifying the neighbor group name using the `neighbor group` command, you can assign options to the neighbor group.

All commands that can be configured under a specified neighbor group can be configured under a neighbor.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family { ipv4 | ipv6 } unicast`
4. `exit`
5. `neighbor-group name`
6. `remote-as as-number`
7. `address-family { ipv4 | ipv6 } unicast`
8. `route-policy route-policy-name { in | out }`
9. `exit`
10. `exit`
11. `neighbor ip-address`
12. `use neighbor-group group-name`
13. `remote-as as-number`
14. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

### Step 2: router bgp as-number

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: address-family { ipv4 | ipv6 } unicast

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```
Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 4: exit

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# exit
```
Exits the current configuration mode.

### Step 5: neighbor-group name

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor-group nbr-grp-A
```
Places the router in neighbor group configuration mode.

### Step 6: remote-as as-number

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbrgrp)# remote-as 2002
```
Creates a neighbor and assigns a remote autonomous system number to it.

### Step 7: address-family { ipv4 | ipv6 } unicast

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbrgrp)# address-family ipv4 unicast
```
Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 8: route-policy route-policy-name { in | out }

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbrgrp-af)# route-policy drop-as-1234 in
```
(Optional) Applies the specified policy to inbound IPv4 unicast routes.

### Step 9: exit

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbrgrp-af)# exit
```
Exits the current configuration mode.

### Step 10: exit

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbrgrp)# exit
```
Exits the current configuration mode.

### Step 11: neighbor ip-address

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```
Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

### Step 12: use neighbor-group group-name

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# use neighbor-group nbr-grp-A
```
(Optional) Specifies that the BGP neighbor inherit configuration from the specified neighbor group.

### Step 13: remote-as as-number

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 2002
```
Creates a neighbor and assigns a remote autonomous system number to it.

### Step 14: Use the commit or end command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

## BGP Neighbor Configuration: Example

The following example shows how BGP neighbors on an autonomous system are configured to share information. In the example, a BGP router is assigned to autonomous system 109, and two networks are listed as originating in the autonomous system. Then the addresses of three remote routers (and their autonomous systems) are listed. The router being configured shares information about networks `172.16.0.0` and `192.168.7.0` with the neighbor routers. The first router listed is in a different autonomous system; the second neighbor and remote-as commands specify an internal neighbor (with the same autonomous system number) at address `172.26.234.2`; and the third neighbor and remote-as commands specify a neighbor on a different autonomous system.

```bash
route-policy pass-all pass end-policy 
router bgp 109 
  address-family ipv4 unicast 
    network 172.16.0.0 255.255.0.0
    network 192.168.7.0 255.255.0.0 
    neighbor 172.16.200.1 
      remote-as 167 
      address-family ipv4 unicast 
        route-policy pass-all in 
        route-policy pass-out out 
    neighbor 172.26.234.2 
      remote-as 109 
      address-family ipv4 unicast 
    neighbor 172.26.64.19 
      remote-as 99 
      address-family ipv4 unicast 
        route-policy pass-all in 
        route-policy pass-all out
```

# Disable BGP Neighbor

Perform this task to administratively shut down a neighbor session without removing the configuration.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `shutdown`
5. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

### Step 2: router bgp as-number

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 127
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: neighbor ip-address

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```
Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

### Step 4: shutdown

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# shutdown
```
Disables all active sessions for the specified neighbor.

### Step 5: Use the commit or end command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

# Resetting Neighbors Using BGP Inbound Soft Reset

Perform this task to trigger an inbound soft reset of the specified address families for the specified group or neighbors. The group is specified by the `*`, `ip-address`, `as-number`, or `external` keywords and arguments.

Resetting neighbors is useful if you change the inbound policy for the neighbors or any other configuration that affects the sending or receiving of routing updates. If an inbound soft reset is triggered, BGP sends a REFRESH request to the neighbor if the neighbor has advertised the ROUTE_REFRESH capability. To determine whether the neighbor has advertised the ROUTE_REFRESH capability, use the `show bgp neighbors` command.

## SUMMARY STEPS

1. `show bgp neighbors`
2. `soft [ in [ prefix-filter ] | out ]`

## DETAILED STEPS

### Purpose Command or Action

Verifies that received route refresh capability from the neighbor is enabled.

### Step 1: show bgp neighbors

Example:
```bash
RP/0/RP0/CPU0:router# show bgp neighbors
```

Soft resets a BGP neighbor.

### Step 2: soft [ in [ prefix-filter ] | out ]

Example:
```bash
RP/0/RP0/CPU0:router# clear bgp ipv4 unicast 10.0.0.1 soft in
```

- The `*` keyword resets all BGP neighbors.
- The `ip-address` argument specifies the address of the neighbor to be reset.
- The `as-number` argument specifies that all neighbors that match the autonomous system number be reset.
- The `external` keyword specifies that all external neighbors are reset.

# Resetting Neighbors Using BGP Outbound Soft Reset

Perform this task to trigger an outbound soft reset of the specified address families for the specified group or neighbors. The group is specified by the `*`, `ip-address`, `as-number`, or `external` keywords and arguments.

Resetting neighbors is useful if you change the outbound policy for the neighbors or any other configuration that affects the sending or receiving of routing updates.

If an outbound soft reset is triggered, BGP resends all routes for the address family to the given neighbors.

To determine whether the neighbor has advertised the ROUTE_REFRESH capability, use the `show bgp neighbors` command.

## SUMMARY STEPS

1. `show bgp neighbors`
2. `soft out`

## DETAILED STEPS

### Purpose Command or Action

Verifies that received route refresh capability from the neighbor is enabled.

### Step 1: show bgp neighbors

Example:
```bash
RP/0/RP0/CPU0:router# show bgp neighbors
```

Soft resets a BGP neighbor.

### Step 2: soft out

Example:
```bash
RP/0/RP0/CPU0:router# clear bgp ipv4 unicast 10.0.0.2 soft out
```

- The `*` keyword resets all BGP neighbors.
- The `ip-address` argument specifies the address of the neighbor to be reset.
- The `as-number` argument specifies that all neighbors that match the autonomous system number be reset.
- The `external` keyword specifies that all external neighbors are reset.

# Reset Neighbors Using BGP Hard Reset

Perform this task to reset neighbors using a hard reset. A hard reset removes the TCP connection to the neighbor, removes all routes received from the neighbor from the BGP table, and then re-establishes the session with the neighbor. If the `graceful` keyword is specified, the routes from the neighbor are not removed from the BGP table immediately, but are marked as stale. After the session is re-established, any stale route that has not been received again from the neighbor is removed.

## SUMMARY STEPS

```bash
clear bgp { ipv4 { unicast | labeled-unicast | all | tunnel tunnel | mdt } | ipv6 unicast | all | labeled-unicast } | all { unicast | multicast | all | labeled-unicast | mdt | tunnel } | vpnv4 unicast | vrf { vrf-name | all } { ipv4 unicast | labeled-unicast } | ipv6 unicast } | vpnv6 unicast } { * | ip-address | as as-number | external } [ graceful ] soft [ in [ prefix-filter ] | out ] clear bgp { ipv4 | ipv6} { unicast | labeled-unicast }
```

## DETAILED STEPS

Example:
```bash
RP/0/RP0/CPU0:router# clear bgp ipv4 unicast 10.0.0.3
```

Clears a BGP neighbor.

- The `*` keyword resets all BGP neighbors.
- The `ip-address` argument specifies the address of the neighbor to be reset.
- The `as-number` argument specifies that all neighbors that match the autonomous system number be reset.
- The `external` keyword specifies that all external neighbors are reset.
- The `graceful` keyword specifies a graceful restart.

# Configure Software to Store Updates from Neighbor

Perform this task to configure the software to store updates received from a neighbor.

The `soft-reconfiguration inbound` command causes a route refresh request to be sent to the neighbor if the neighbor is route refresh capable. If the neighbor is not route refresh capable, the neighbor must be reset to relearn received routes using the `clear bgp soft` command.

**Note:** Storing updates from a neighbor works only if either the neighbor is route refresh capable or the `soft-reconfiguration inbound` command is configured. Even if the neighbor is route refresh capable and the `soft-reconfiguration inbound` command is configured, the original routes are not stored unless the `always` option is used with the command. The original routes can be easily retrieved with a route refresh request. Route refresh sends a request to the peer to resend its routing information. The `soft-reconfiguration inbound` command stores all paths received from the peer in an unmodified form and refers to these stored paths during the clear. Soft reconfiguration is memory intensive.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `address-family { ipv4 | ipv6 } unicast`
5. `soft-reconfiguration inbound [ always]`
6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

### Step 2: router bgp as-number

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: neighbor ip-address

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```
Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

### Step 4: address-family { ipv4 | ipv6 } unicast

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
```
Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 5: soft-reconfiguration inbound [ always]

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# soft-reconfiguration inbound always
```
Configures the software to store updates received from a specified neighbor. Soft reconfiguration inbound causes the software to store the original unmodified route in addition to a route that is modified or filtered. This allows a “soft clear” to be performed after the inbound policy is changed.

Soft reconfiguration enables the software to store the incoming updates before apply policy if route refresh is not supported by the peer (otherwise a copy of the update is not stored). The `always` keyword forces the software to store a copy even when route refresh is supported by the peer.

### Step 6: Use the commit or end command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

# Log Neighbor Changes

Logging neighbor changes is enabled by default. Use the `bgp log neighbor changes disable` command to turn off logging. Use the `no bgp log neighbor changes disable` command to turn logging back on, if it has been disabled.
```
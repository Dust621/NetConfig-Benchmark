```markdown
# BGP Routing Domain Confederation

One way to reduce the iBGP mesh is to divide an autonomous system into multiple sub-autonomous systems and group them into a single confederation. To the outside world, the confederation looks like a single autonomous system. Each autonomous system is fully meshed within itself and has a few connections to other autonomous systems in the same confederation.

Although the peers in different autonomous systems have eBGP sessions, they exchange routing information as if they were iBGP peers. Specifically, the next hop, MED, and local preference information is preserved. This feature allows you to retain a single IGP for all of the autonomous systems.

## Configure Routing Domain Confederation for BGP

Perform this task to configure the routing domain confederation for BGP. This includes specifying a confederation identifier and autonomous systems that belong to the confederation.

Configuring a routing domain confederation reduces the internal BGP (iBGP) mesh by dividing an autonomous system into multiple autonomous systems and grouping them into a single confederation. Each autonomous system is fully meshed within itself and has a few connections to another autonomous system in the same confederation.

The confederation maintains the next hop and local preference information, and that allows you to retain a single Interior Gateway Protocol (IGP) for all autonomous systems. To the outside world, the confederation looks like a single autonomous system.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `bgp confederation identifier as-number`
4. `bgp confederation peers as-number`
5. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: `bgp confederation identifier as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation identifier 5
```

Specifies a BGP confederation identifier.

### Step 4: `bgp confederation peers as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1091
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1092
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1093
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1094
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1095
RP/0/RP0/CPU0:router(config-bgp)# bgp confederation peers 1096
```

Specifies that the BGP autonomous systems belong to a specified BGP confederation identifier. You can associate multiple AS numbers to the same confederation identifier, as shown in the example.

### Step 5: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## BGP Confederation: Example

The following is a sample configuration that shows several peers in a confederation. The confederation consists of three internal autonomous systems with autonomous system numbers 6001, 6002, and 6003. To the BGP speakers outside the confederation, the confederation looks like a normal autonomous system with autonomous system number 666 (specified using the `bgp confederation identifier` command).

In a BGP speaker in autonomous system 6001, the `bgp confederation peers` command marks the peers from autonomous systems 6002 and 6003 as special eBGP peers. Hence, peers `171.16.232.55` and `171.16.232.56` get the local preference, next hop, and MED unmodified in the updates. The router at `171.19.69.1` is a normal eBGP speaker, and the updates received by it from this peer are just like a normal eBGP update from a peer in autonomous system 666.

```bash
router bgp 6001
 bgp confederation identifier 666
 bgp confederation peers 6002 6003
 exit
 address-family ipv4 unicast
  neighbor 171.16.232.55 remote-as 6002
 exit
 address-family ipv4 unicast
  neighbor 171.16.232.56 remote-as 6003
 exit
 address-family ipv4 unicast
  neighbor 171.19.69.1 remote-as 777
```

In a BGP speaker in autonomous system 6002, the peers from autonomous systems 6001 and 6003 are configured as special eBGP peers. Peer `171.17.70.1` is a normal iBGP peer, and peer `199.99.99.2` is a normal eBGP peer from autonomous system 700.

```bash
router bgp 6002
 bgp confederation identifier 666
 bgp confederation peers 6001 6003
 exit
 address-family ipv4 unicast
  neighbor 171.17.70.1 remote-as 6002
 exit
 address-family ipv4 unicast
  neighbor 171.19.232.57 remote-as 6001
 exit
 address-family ipv4 unicast
  neighbor 171.19.232.56 remote-as 6003
 exit
 address-family ipv4 unicast
  neighbor 171.19.99.2 remote-as 700
 exit
 address-family ipv4 unicast
  route-policy pass-all in
  route-policy pass-all out
```

In a BGP speaker in autonomous system 6003, the peers from autonomous systems 6001 and 6002 are configured as special eBGP peers. Peer `192.168.200.200` is a normal eBGP peer from autonomous system 701.

```bash
router bgp 6003
 bgp confederation identifier 666
 bgp confederation peers 6001 6002
 exit
 address-family ipv4 unicast
  neighbor 171.19.232.57 remote-as 6001
 exit
 address-family ipv4 unicast
  neighbor 171.19.232.55 remote-as 6002
 exit
 address-family ipv4 unicast
  neighbor 192.168.200.200 remote-as 701
 exit
 address-family ipv4 unicast
  route-policy pass-all in
  route-policy pass-all out
```

The following is a part of the configuration from the BGP speaker `192.168.200.205` from autonomous system 701 in the same example. Neighbor `171.16.232.56` is configured as a normal eBGP speaker from autonomous system 666. The internal division of the autonomous system into multiple autonomous systems is not known to the peers external to the confederation.

```bash
router bgp 701
 address-family ipv4 unicast
  neighbor 172.16.232.56 remote-as 666
 exit
 address-family ipv4 unicast
  route-policy pass-all in
  route-policy pass-all out
 exit
 address-family ipv4 unicast
  neighbor 192.168.200.205 remote-as 701
```
```
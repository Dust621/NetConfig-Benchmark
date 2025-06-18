```markdown
# Verify Networking and Routing Problems

Perform this task to verify the operation of routes between nodes.

## SUMMARY STEPS

1. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] [ protocol [ instance ] | ip-address mask ] [ standby ] [ detail ]`
2. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] backup [ ip-address ] [ standby ]`
3. `show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] best-local ip-address [ standby ]`
4. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] connected [ standby ]`
5. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] local [ interface ] [ standby ]`
6. `show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] longer-prefixes { ip-address mask | ip-address / prefix-length } [ standby ]`
7. `show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] next-hop ip-address [ standby ]`

## DETAILED STEPS

### Step 1

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] [ protocol [ instance ] | ip-address mask ] [ standby ] [ detail ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast 192.168.1.11/8
```

Displays the current routes in RIB.

### Step 2

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] backup [ ip-address ] [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast backup 192.168.1.11/8
```

Displays backup routes in RIB.

### Step 3

```bash
show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] best-local ip-address [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast best-local 192.168.1.11/8
```

Displays the best-local address to use for return packets from the given destination.

### Step 4

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] connected [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast connected
```

Displays the current connected routes of the routing table.

### Step 5

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] local [ interface ] [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast local
```

Displays local routes for receive entries in the routing table.

### Step 6

```bash
show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] longer-prefixes { ip-address mask | ip-address / prefix-length } [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast longer-prefixes 192.168.1.11/8
```

Displays the current routes in RIB that share a given number of bits with a given network.

### Step 7

```bash
show route [ vrf { vrf-name | all }] [ ipv4 | ipv6 ] [ unicast | safi-all ] next-hop ip-address [ standby ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast next-hop 192.168.1.34
```

Displays the next-hop gateway or host to a destination address.

## Output of `show route` Command: Example

The following is sample output from the `show route` command when entered without an address:

```bash
show route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
O - OSPF, IA - OSPF inter area
N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
U - per-user static route, o - ODR, L - local
Gateway of last resort is 172.23.54.1 to network 0.0.0.0

C 10.2.210.0/24 is directly connected, 1d21h, Ethernet0/1/0/0
L 10.2.210.221/32 is directly connected, 1d21h, Ethernet0/1/1/0
C 172.20.16.0/24 is directly connected, 1d21h, ATM4/0.1
L 172.20.16.1/32 is directly connected, 1d21h, ATM4/0.1
C 10.6.100.0/24 is directly connected, 1d21h, Loopback1
L 10.6.200.21/32 is directly connected, 1d21h, Loopback0
S 192.168.40.0/24 [1/0] via 172.20.16.6, 1d21h
```
```
```markdown
# Enabling BGP Unequal Cost Recursive Load Balancing

Perform this task to enable unequal cost recursive load balancing for external BGP (eBGP) and eiBGP and to enable BGP to carry link bandwidth attribute of the demilitarized zone (DMZ) link.

When the PE router includes the link bandwidth extended community in its updates to the remote PE through the Multiprotocol Interior BGP (MP-iBGP) session (either IPv4 or VPNv4), the remote PE automatically does load balancing if the `maximum-paths` command is enabled.

Unequal cost recursive load balancing happens across maximum eight paths only.

**Note**: Enabling BGP unequal cost recursive load balancing feature is not supported on CPP based cards.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family { ipv4 | ipv6 } unicast`
4. `maximum-paths { ebgp | ibgp | eibgp } maximum [ unequal-cost ]`
5. `exit`
6. `neighbor ip-address`
7. `dmz-link-bandwidth`
8. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: Enters mode.

```bash
configure
```

**Example**:
```bash
RP/0/RP0/CPU0:router# configure
```

---

### Step 2: Specifies the autonomous system number and enters the BGP configuration mode.

```bash
router bgp as-number
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

---

### Step 3: Specifies either an IPv4 or IPv6 address family unicast.

```bash
address-family { ipv4 | ipv6 } unicast
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```

**Note**: To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

---

### Step 4: Configures the maximum number of parallel routes that BGP installs.

```bash
maximum-paths { ebgp | ibgp | eibgp } maximum [ unequal-cost ]
```

**Examples**:
- `ebgp maximum`: Consider only eBGP paths for multipath.
  ```bash
  RP/0/RP0/CPU0:router(config-bgp-af)# maximum-paths ebgp 3
  ```
- `ibgp maximum [ unequal-cost ]`: Consider load balancing between iBGP learned paths.
- `eibgp maximum`: Consider both eBGP and iBGP learned paths for load balancing. eiBGP load balancing always does unequal-cost load balancing.

**Note**: When eiBGP is applied, eBGP or iBGP load balancing cannot be configured; however, eBGP and iBGP load balancing can coexist.

---

### Step 5: Exits the current configuration mode.

```bash
exit
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# exit
```

---

### Step 6: Configures a CE neighbor.

```bash
neighbor ip-address
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 10.0.0.1
```

---

### Step 7: Originates a DMZ link-bandwidth extended community.

```bash
dmz-link-bandwidth
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# dmz-link-bandwidth
```

---

### Step 8: Commits or ends the configuration.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes**: Saves configuration changes and exits the configuration session.
  - **No**: Exits the configuration session without committing the configuration changes.
  - **Cancel**: Remains in the configuration session, without committing the configuration changes.

---

## DMZ Link Bandwidth for Unequal Cost Recursive Load Balancing

The demilitarized zone (DMZ) link bandwidth for unequal cost recursive load balancing feature provides support for unequal cost load balancing for recursive prefixes on local node using DMZ link bandwidth. Use the `dmz-link-bandwidth` command in BGP neighbor configuration mode and the `bandwidth` command in interface configuration mode to achieve unequal load balance.

When the PE router includes the link bandwidth extended community in its updates to the remote PE through the MP-iBGP session, the remote PE automatically does load balancing if the `maximum-paths` command is enabled.

**Note**: Unequal cost recursive load balancing happens across maximum eight paths only.

---

## BGP Unequal Cost Recursive Load Balancing: Example

This is a sample configuration for unequal cost recursive load balancing:

```bash
interface Loopback0
 ipv4 address 20.20.20.20 255.255.255.255
!
interface MgmtEth0/RSP0/CPU0/0
 ipv4 address 8.43.0.10 255.255.255.0
!
interface TenGigE0/3/0/0
 bandwidth 8000000
 ipv4 address 11.11.11.11 255.255.255.0
 ipv6 address 11:11:0:1::11/64
!
interface TenGigE0/3/0/1
 bandwidth 7000000
 ipv4 address 11.11.12.11 255.255.255.0
 ipv6 address 11:11:0:2::11/64
!
interface TenGigE0/3/0/2
 bandwidth 6000000
 ipv4 address 11.11.13.11 255.255.255.0
 ipv6 address 11:11:0:3::11/64
!
interface TenGigE0/3/0/3
 bandwidth 5000000
 ipv4 address 11.11.14.11 255.255.255.0
 ipv6 address 11:11:0:4::11/64
!
interface TenGigE0/3/0/4
 bandwidth 4000000
 ipv4 address 11.11.15.11 255.255.255.0
 ipv6 address 11:11:0:5::11/64
!
interface TenGigE0/3/0/5
 bandwidth 3000000
 ipv4 address 11.11.16.11 255.255.255.0
 ipv6 address 11:11:0:6::11/64
!
interface TenGigE0/3/0/6
 bandwidth 2000000
 ipv4 address 11.11.17.11 255.255.255.0
 ipv6 address 11:11:0:7::11/64
!
interface TenGigE0/3/0/7
 bandwidth 1000000
 ipv4 address 11.11.18.11 255.255.255.0
 ipv6 address 11:11:0:8::11/64
!
interface TenGigE0/4/0/0
 description CONNECTED TO IXIA 1/3
 transceiver permit pid all
!
interface TenGigE0/4/0/2
 ipv4 address 9.9.9.9 255.255.0.0
 ipv6 address 9:9::9/64
 ipv6 enable
!
route-policy pass-all
 pass
end-policy
!
router static
 address-family ipv4 unicast
  202.153.144.0/24 8.43.0.1
!
!
router bgp 100
 bgp router-id 20.20.20.20
 address-family ipv4 unicast
  maximum-paths eibgp 8
  redistribute connected
 !
 neighbor 11.11.11.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.12.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.13.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.14.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.15.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.16.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.17.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
 !
 neighbor 11.11.18.12
  remote-as 200
  dmz-link-bandwidth
  address-family ipv4 unicast
   route-policy pass-all in
   route-policy pass-all out
 !
!
!
end
```

---

## DMZ Link Bandwidth Over EBGP Peer

The demilitarized zone (DMZ) link bandwidth extended community is an optional non-transitive attribute; therefore, it is not advertised to eBGP peers by default but it is advertised only to iBGP peers. This extended community is meant for load balancing over multi-paths. However, Cisco IOS-XR enables advertising of the DMZ link bandwidth to an eBGP peer, or receiving the DMZ link bandwidth by an eBGP peer. This feature also gives the user the option to send the bandwidth unchanged, or take the accumulated bandwidth over all the egress links and advertise that to the upstream eBGP peer.

Use the `ebgp-send-community-dmz` command to send the community to eBGP peers. By default, the link bandwidth extended-community attribute associated with the best path is sent.

When the `cumulative` keyword is used, the value of the link bandwidth extended community is set to the sum of link bandwidth values of all the egress-multipaths. If the DMZ link bandwidth value of the multipaths is unknown, for instance, some paths do not have that attribute, then unequal cost load-balancing is not done at that node. However, the sum of the known DMZ link bandwidth values is calculated and sent to the eBGP peer.

Use the `ebgp-recv-community-dmz` command to receive the community from eBGP peers.

**Note**: The `ebgp-send-community-dmz` and `ebgp-recv-community-dmz` commands can be configured in the neighbor, neighbor-group, and session-group configuration mode.

Use the `bgp bestpath as-path multipath-relax` and `bgp bestpath as-path ignore` commands to handle multipath across different autonomous systems.

---

## Sending and Receiving DMZ Link Bandwidth Extended Community over eBGP Peer

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `neighbor ip-address`
4. `ebgp-send-extcommunity-dmz ip-address`
5. `exit`
6. `neighbor ip-address`
7. `ebgp-recv-extcommunity-dmz`
8. `exit`

### DETAILED STEPS

#### Step 1: Enters mode.

```bash
configure
```

**Example**:
```bash
RP/0/RP0/CPU0:router# configure
```

---

#### Step 2: Specifies the autonomous system number.

```bash
router bgp as-number
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```

---

#### Step 3: Configures BGP neighbor.

```bash
neighbor ip-address
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 10.1.1.1
```

---

#### Step 4: Sends DMZ link bandwidth extended community.

```bash
ebgp-send-extcommunity-dmz ip-address
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp)# ebgp-send-extcommunity-dmz
```

**Note**: Use the `cumulative` keyword with this command to set the value of the link bandwidth extended community to the sum of link bandwidth values of all the egress multipaths.

---

#### Step 5: Exits neighbor configuration mode.

```bash
exit
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# exit
```

---

#### Step 6: Configures another BGP neighbor.

```bash
neighbor ip-address
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.16.0.1
```

---

#### Step 7: Receives DMZ link bandwidth extended community.

```bash
ebgp-recv-extcommunity-dmz
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# ebgp-recv-extcommunity-dmz
```

---

#### Step 8: Exits neighbor configuration mode.

```bash
exit
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# exit
```

---

## DMZ Link Bandwidth: Example

The following examples show how Router R1 sends DMZ link bandwidth extended communities to Router R2 over eBGP peer connection:

**R1: sending router**
```bash
neighbor 10.3.3.3 remote-as 2
ebgp-send-extcommunity-dmz
address-family ipv4 unicast
 route-policy pass in
 route-policy pass out
!
```

**R2: Receiving router**
```bash
neighbor 192.0.2.1 remote-as 3
ebgp-recv-extcommunity-dmz
address-family ipv4 unicast
 route-policy pass in
 route-policy pass out
!
```

The following is a sample configuration that displays the DMZ link bandwidth configuration in the sending (R1) router:

```bash
RP/0/RP0/CPU0:router)# show bgp ipv4 unicast 10.1.1.1/32 detail

Path #1: Received by speaker 0
Flags: 0x4000000001040003, import: 0x20
Advertised to update-groups (with more than one peer): 0.4
Advertised to peers (in unique update groups): 20.0.0.1
3 11.1.0.2 from 11.1.0.2 (11.1.0.2)
Origin incomplete, metric 20, localpref 100, valid, external, best, group-best
Received Path ID 0, Local Path ID 0, version 21
Extended community: LB:3:192
Origin-AS validity: not-found
```

The following is a sample configuration that displays DMZ link bandwidth configuration in the receiving (R2) router:

```bash
RP/0/RP0/CPU0:router)# show bgp ipv4 unicast 10.1.1.1/32 detail

Paths: (1 available, best #1)
Not advertised to any peer
Path #1: Received by speaker 0
Not advertised to any peer
1 3 20.0.0.2 from 20.0.0.2 (10.0.0.81)
Origin incomplete, localpref 100, valid, external, best, group-best
Received Path ID 0, Local Path ID 0, version 17
Extended community: LB:1:192
Origin-AS validity: not-found
```
```
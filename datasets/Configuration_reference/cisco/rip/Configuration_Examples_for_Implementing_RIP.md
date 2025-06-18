# Configuration Examples for Implementing RIP

This section provides the following configuration examples:

## Configuring a Basic RIP Configuration: Example

The following example shows two Gigabit Ethernet interfaces configured with RIP.

```bash
interface TenGigE 0/3/0/0
ipv4 address 172.16.0.1 255.255.255.0
!
interface TenGigE 0/3/0/1
ipv4 address 172.16.2.12 255.255.255.0
!
router rip
interface TenGigE 0/3/0/0
!
interface TenGigE 0/3/0/1
!
```

## Configuring RIP on the Provider Edge: Example

The following example shows how to configure basic RIP on the PE with two VPN routing and forwarding (VRF) instances.

```bash
router rip
interface HundredGigE 0/1/0/3
!
vrf vpn0
interface HundredGigE 0/1/0/4
!
!
vrf vpn1
interface HundredGigE 0/1/0/5
!
!
```

## Adjusting RIP Timers for each VRF Instance: Example

The following example shows how to adjust RIP timers for each VPN routing and forwarding (VRF) instance.

For VRF instance `vpn0`, the `timers basic` command sets updates to be broadcast every 10 seconds. If a router is not heard from in 30 seconds, the route is declared unusable. Further information is suppressed for an additional 30 seconds. At the end of the flush period (45 seconds), the route is flushed from the routing table.

For VRF instance `vpn1`, timers are adjusted differently: 20, 60, 60, and 70 seconds.

The `output-delay` command changes the interpacket delay for RIP updates to 10 milliseconds on `vpn1`. The default is that interpacket delay is turned off.

```bash
router rip
interface HundredGigE 0/1/0/3
!
vrf vpn0
interface HundredGigE 0/1/0/4
!
timers basic 10 30 30 45
!
vrf vpn1
interface HundredGigE 0/1/0/5
!
timers basic 20 60 60 70
output-delay 10
!
!
```

## Configuring Redistribution for RIP: Example

The following example shows how to redistribute Border Gateway Protocol (BGP) and static routes into RIP.

The RIP metric used for redistributed routes is determined by the route policy. If a route policy is not configured or the route policy does not set RIP metric, the metric is determined based on the redistributed protocol. For VPNv4 routes redistributed by BGP, the RIP metric set at the remote PE router is used, if valid.

In all other cases (BGP, IS-IS, OSPF, connected, static), the metric set by the `default-metric` command is used. If a valid metric cannot be determined, then redistribution does not happen.

```bash
route-policy ripred
set rip-metric 5
end-policy
!
router rip
vrf vpn0
interface HundredGigE 0/1/0/3
!
redistribute connected
default-metric 3
!
vrf vpn1
interface HundredGigE 0/1/0/4
!
redistribute bgp 100 route-policy ripred
redistribute static
default-metric 3
!
!
```

## Configuring Route Policies for RIP: Example

The following example shows how to configure inbound and outbound route policies that are used to control which route updates are received by a RIP interface or sent out from a RIP interface.

```bash
prefix-set pf1
10.1.0.0/24
end-set
!
prefix-set pf2
150.10.1.0/24
end-set
!
route-policy policy_in
if destination in pf1 then
pass
endif
end-policy
!
route-policy pass-all
pass
end-policy
!
route-policy infil
if destination in pf2 then
add rip-metric 2
pass
endif
end-policy
!
router rip
interface HundredGigE 0/1/0/3
route-policy policy_in in
!
interface HundredGigE 0/1/0/4
!
route-policy infil in
route-policy pass-all out
```

## Configuring Passive Interfaces and Explicit Neighbors for RIP: Example

The following example shows how to configure passive interfaces and explicit neighbors. When an interface is passive, it only accepts routing updates. In other words, no updates are sent out of an interface except to neighbors configured explicitly.

```bash
router rip
interface HundredGigE 0/1/0/3
passive-interface
!
interface HundredGigE 0/1/0/4
!
neighbor 172.17.0.1
neighbor 172.18.0.5
!
```
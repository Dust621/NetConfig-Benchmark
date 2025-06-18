```markdown
# Multihop BFD over BVI

## Feature History Table

| Feature Name                                      | Release   | Information                                                                 |
|---------------------------------------------------|-----------|-----------------------------------------------------------------------------|
| Multihop BFD over Bridge Group Virtual Interface (BVI) | 7.4.1     | Introduces support for multihop BFD over BVI, enabling BFD sessions between endpoints with IP connectivity. |

## Feature Description

The multihop BFD over Bridge Group Virtual Interface (BVI) feature introduces support for multihop BFD over BVI. You can set up a multihop BFD session between two endpoints that have IP connectivity. This session is between a unique source-destination address pair that the client provides.

This feature allows you to extend BFD on arbitrary paths. These arbitrary paths can span multiple network hops, hence detecting link failures.

Multihop BFD over BVI feature allows you to configure both routing and bridging on the same interface using Integrated Routing Bridging (IRB). IRB enables you to route between a bridged domain and a routed domain with the Bridge Group Virtual Interface (BVI).

The BVI is a virtual interface within the router that acts like a normal, routed interface that does not support bridging, but represents the comparable bridge group to routed interfaces within the router.

## Restrictions

- The minimum Multihop BFD timer for the BVI interface is 50 msec.
- The `multihop ttl-drop-threshold` command is not supported.
- The Multihop BFD over BVI or IRB functionality is supported only in asynchronous mode and does not support echo mode.
- The Multihop BFD over BVI feature is not supported over MPLS and SR core.

## Supported Functionality

- This feature is supported in both IPv4 and IPv6.
- BFD Multihop over BVI feature supports on client BGP.
- BFD Multihop supports only over IP core.
- BFD Multihop supports on all currently supported media-type for BFD single-hop.

## Configuration

### Configure BVI Interface

```bash
/* Configure a BVI interface and assign an IP address */
Router(config)# interface BVI1
Router(config-if)# host-routing
Router(config-if)# mtu 8986
Router(config-if)# ipv4 address 10.1.1.1 255.255.255.0
Router(config-if)# ipv6 address 10:1:1::1/120
```

### Configure Layer 2 AC Interface

```bash
/* Configure the Layer 2 AC interface */
Router(config-if)# interface TenGigE0/5/0/6/0.1 l2transport
Router(config-subif)# encapsulation dot1q 1
Router(config-subif)# rewrite ingress tag pop 1 symmetric
```

### Configure L2VPN Bridge Domain

```bash
/* Configure L2VPN Bridge Domain */
Router(config-subif)# l2vpn
Router(config-subif)# bridge group 1
Router(config-subif)# bridge-domain 1
Router(config-l2vpn-bg-bd)# interface TenGigE0/5/0/6/0.1
Router(config-l2vpn-bg-bd)# routed interface BVI1
```

## Running Configuration

```bash
interface BVI1
 host-routing
 mtu 8986
 ipv4 address 10.1.1.1 255.255.255.0
 ipv6 address 10:1:1::1/120
!
interface TenGigE0/5/0/6/0.1 l2transport
 encapsulation dot1q 1
 rewrite ingress tag pop 1 symmetric
!
l2vpn
 bridge group 1
 bridge-domain 1
  interface TenGigE0/5/0/6/0.1
 !
 routed interface BVI1
!
```

Repeat the configuration on the peer router.

### Configure BGP as the Routing Protocol

```bash
/* Configure BGP as the routing protocol */
Router(config)# router bgp 1
Router(config-bgp)# neighbor 2.2.1.1
Router(config-bgp-nbr)# remote-as 1
Router(config-bgp-nbr)# bfd fast-detect
Router(config-bgp-nbr)# bfd minimum-interval 300
Router(config-bgp-nbr)# update-source Loopback1
Router(config-bgp-nbr)# address-family ipv4 unicast
```

### Configure Reachability to the BGP Neighbor IP

```bash
/* Configure reachability to the BGP neighbour IP either via static or IGP */
Router(config-bgp-nbr-af)# router static
Router(config-static)# address-family ipv4 unicast
Router(config-static-afi)# 2.2.1.1/32 10.1.1.2
```

### Configure Line Cards for Multipath BFD Sessions

```bash
/* Configure the line cards to allow hosting of Multipath BFD sessions. */
Router(config-static-afi)# bfd
Router(config-bfd)#
router bgp 1
 neighbor 2.2.1.1
  remote-as 1
  bfd fast-detect
  bfd minimum-interval 300
  update-source Loopback1
  address-family ipv4 unicast
 !
router static
 address-family ipv4 unicast
  2.2.1.1/32 10.1.1.2
 !
bfd
 multipath include location !
```

> **Note:** To avoid the unsupported three-level recursion on BVI interfaces on the first and second generation of line cards, you must not configure the BVI interface as the next-hop in the static route configuration.

## Verification

```bash
Router# show bfd session destination 2.2.1.1
Fri May 28 14:35:52.566 IST

Src Addr       Dest Addr      VRF Name       H/W NPU       Local det time(int*mult)      State      Echo      Async
-------------- -------------- -------------- -------------- ---------------------------- ---------- --------- ---------
1.1.1.1        2.2.1.1        default        Yes           n/a                          900ms(300ms*3) UP
```
```
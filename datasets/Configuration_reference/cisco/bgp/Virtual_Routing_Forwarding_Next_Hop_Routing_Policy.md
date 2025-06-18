```markdown
# Virtual Routing Forwarding Next Hop Routing Policy

## Table 8: Feature History Table

| Description | Release Name | Feature Name |
|------------|-------------|--------------|
| Introduced in this release on: NCS 5500 modular routers (NCS 5500 line cards) | Release 7.11.1 | Virtual Routing Forwarding Next Hop Routing Policy |

You can now enable a route policy at the BGP next-hop attach point to limit notifications delivered to BGP for specific prefixes, which equips you with better control over routing decisions, and allows for precise traffic engineering and security compliance for each VRF instance, and helps establish redundant paths specific to each VRF.

The feature introduces these changes:

### CLI

**Modified Command:**

- The `nexthop route-policy` command is extended to VRF address-family configuration mode.

### YANG Data Model

- New XPaths for:
  - `Cisco-IOS-XR-ipv4-bgp-cfg.yang`
  - `Cisco-IOS-XR-um-router-bgp-cfg`  
  *(see GitHub, YANG Data Models Navigator)*

## Overview

This functionality enables the extension of BGP capabilities by permitting the configuration of next-hop route policies on specific VRFs. A technique within BGP route policies allows limiting notifications for specific prefixes, optimizing BGP routing within a VRF. When dealing with scenarios requiring VRF-specific route policies for BGP, configuring a route policy at the BGP next-hop attach point becomes crucial.

The following are some of the benefits of applying next-hop route policies on individual VRFs:

- Enabling next-hop route policies at the Virtual Routing and Forwarding (VRF) instances level provides network administrators with better control over routing decisions within each VRF instance.
  
- Implementing next-hop route policies within VRF instances allows for precise traffic engineering and optimization management. VRFs might have specific traffic routing requirements, taking into account criteria like latency, bandwidth, or preferred routes.

- Implementing policies on individual VRF instances assures precise security compliance, addressing unique VRF needs. Traffic adheres strictly, following defined rules and access controls.

- Configuring next-hop route policies at the VRF level is critical for establishing failover mechanisms or redundant paths specific to each VRF. This ensures high availability and reliability within the VRF boundaries.

## Configure VRF Next Hop Policy

To enable next hop route policy on a VRF table, perform the following steps:

1. Configure a route policy and enter route-policy configuration mode.
2. Define the route policy to help limit notifications delivered to BGP for specific prefixes.
3. Drop the prefix of the routes that matches the conditions set in the route policy.
4. Enable BGP routing and enter the router configuration mode.
5. Configure a VRF.
6. Configure an IPv4 or IPv6 address family.
7. Configure route policy filtering using next hops.

```bash
Router(config)# route-policy nh-route-policy
Router(config-rpl)# if destination in (10.1.1.0/24) and protocol in (connected, static) then
Router(config-rpl-if)# drop
Router(config-rpl-if)# endif
Router(config-rpl)# end-policy
Router(config-rpl)# exit
Router(config)# router bgp 500
Router(config-bgp)# vrf vrf10
Router(config-bgp-vrf)# address-family ipv4 unicast
Router(config-bgp-vrf-af)# nexthop route-policy nh-route-policy
```

## Running Configuration

```bash
route-policy nh-route-policy
  if destination in (10.1.1.0/24) and protocol in (connected, static) then
    drop
  endif
end-policy
!
router bgp 500
  vrf vrf10
    address-family ipv4 unicast
      nexthop route-policy nh-route-policy
```

## Verification

Verify that the configured next route hop policy is enabled in a VRF table. The "BGP table nexthop route policy" field indicates the route policy used to determine the next hop for BGP routes in the specified VRF instance VRF1.

```bash
Router# show bgp vrf vrf1 ipv4 unicast
Fri Jul 7 15:51:16.309 +0530
BGP VRF vrf1, state: Active
BGP Route Distinguisher: 1:1
VRF ID: 0x6000000b
BGP router identifier 10.1.1.1, local AS number 65001
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe000000b
RD version: 1356
BGP table nexthop route policy: nh-route-policy --> This is the same route policy that was configured.
BGP main routing table version 1362
BGP NSR Initial initsync version 1355 (Reached)
BGP NSR/ISSU Sync-Group versions 1362/0
```

**Status codes:**  
`s` suppressed, `d` damped, `h` history, `*` valid, `>` best  
`i` - internal, `r` RIB-failure, `S` stale, `N` Nexthop-discard  

**Origin codes:**  
`i` - IGP, `e` - EGP, `?` - incomplete  

| Network        | Next Hop  | Metric | LocPrf | Weight | Path | Route Distinguisher: 1:1 (default for vrf vrf1) | Route Distinguisher Version: 1356 |
|----------------|-----------|--------|--------|--------|------|------------------------------------------------|-----------------------------------|
| *> 10.1.1.0/24 | 0.0.0.0   | 0      | 32768  | ?      |      |                                                |                                   |
| *> 192.0.2.0/24 | 10.1.1.1 | 0      | 32768  | ?      |      |                                                |                                   |
| *> 198.50.100.0/24 | 10.1.1.1 | 0      | 101    | i      |      |                                                |                                   |
```
```markdown
# Configure BGP Accept Own

The BGP Accept Own feature allows you to handle self-originated VPN routes, which a BGP speaker receives from a route-reflector (RR). A 'self-originated' route is one which was originally advertised by the speaker itself. 

As per BGP protocol [RFC4271], a BGP speaker rejects advertisements that were originated by the speaker itself. However, the BGP Accept Own mechanism enables a router to accept the prefixes it has advertised, when reflected from a route-reflector that modifies certain attributes of the prefix. A special community called ACCEPT-OWN is attached to the prefix by the route-reflector, which is a signal to the receiving router to bypass the ORIGINATOR_ID and NEXTHOP/MP_REACH_NLRI check.

Generally, the BGP speaker detects prefixes that are self-originated through the self-origination check (ORIGINATOR_ID, NEXTHOP/MP_REACH_NLRI) and drops the received updates. However, with the Accept Own community present in the update, the BGP speaker handles the route.

## Applications of BGP Accept Own

One of the applications of BGP Accept Own is auto-configuration of extranets within MPLS VPN networks. In an extranet configuration, routes present in one VRF is imported into another VRF on the same PE. 

Normally, the extranet mechanism requires that either the import-rt or the import policy of the extranet VRFs be modified to control import of the prefixes from another VRF. However, with Accept Own feature, the route-reflector can assert that control without the need for any configuration change on the PE. This way, the Accept Own feature provides a centralized mechanism for administering control of route imports between different VRFs.

## Supported Address Families

BGP Accept Own is supported only for VPNv4 and VPNv6 address families in neighbor configuration mode.

## Configuration Steps

### SUMMARY STEPS

1. configure  
2. router bgp as-number  
3. neighbor ip-address  
4. remote-as as-number  
5. update-source type interface-path-id  
6. address-family {vpnv4 unicast | vpnv6 unicast}  
7. accept-own [inheritance-disable]  

### DETAILED STEPS

**Step 1** configure  

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

**Step 2** router bgp as-number  

Example:

```bash
RP/0/RP0/CPU0:router(config)#router bgp 100
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** neighbor ip-address  

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)#neighbor 10.1.2.3
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

**Step 4** remote-as as-number  

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)#remote-as 100
```

Assigns a remote autonomous system number to the neighbor.

**Step 5** update-source type interface-path-id  

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)#update-source Loopback0
```

Allows sessions to use the primary IP address from a specific interface as the local address when forming a session with a neighbor.

**Step 6** address-family {vpnv4 unicast | vpnv6 unicast}  

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)#address-family vpnv6 unicast
```

Specifies the address family as VPNv4 or VPNv6 and enters neighbor address family configuration mode.

**Step 7** accept-own [inheritance-disable]  

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)#accept-own
```

Enables handling of self-originated VPN routes containing Accept_Own community.

Use the `inheritance-disable` keyword to disable the "accept own" configuration and to prevent inheritance of "acceptown" from a parent configuration.

## BGP Accept Own Configuration: Example

In this configuration example:

- PE11 is configured with Customer VRF and Service VRF.
- OSPF is used as the IGP.
- VPNv4 unicast and VPNv6 unicast address families are enabled between the PE and RR neighbors and IPv4 and IPv6 are enabled between PE and CE neighbors.

The Accept Own configuration works as follows:

1. CE1 originates prefix X.
2. Prefix X is installed in customer VRF as (RD1:X).
3. Prefix X is advertised to IntraAS-RR11 as (RD1:X, RT1).
4. IntraAS-RR11 advertises X to InterAS-RR1 as (RD1:X, RT1).
5. InterAS-RR1 attaches RT2 to prefix X on the inbound and ACCEPT_OWN community on the outbound and advertises prefix X to IntraAS-RR31.
6. IntraAS-RR31 advertises X to PE11.
7. PE11 installs X in Service VRF as (RD2:X,RT1, RT2, ACCEPT_OWN).

### Example: BGP Accept Own on a PE Router

```bash
router bgp 100
 neighbor 45.1.1.1
  remote-as 100
  update-source Loopback0
  address-family vpnv4 unicast
   route-policy pass-all in
   accept-own
   route-policy drop_111.x.x.x out
  !
  address-family vpnv6 unicast
   route-policy pass-all in
   accept-own
   route-policy drop_111.x.x.x out
  !
 !
```

### Example: InterAS-RR Configuration for BGP Accept Own

```bash
router bgp 100
 neighbor 45.1.1.1
  remote-as 100
  update-source Loopback0
  address-family vpnv4 unicast
   route-policy rt_stitch1 in
   route-reflector-client
   route-policy add_bgp_ao out
  !
  address-family vpnv6 unicast
   route-policy rt_stitch1 in
   route-reflector-client
   route-policy add_bgp_ao out
  !
 !
 extcommunity-set rt cs_100:1
  100:1
 end-set
 !
 extcommunity-set rt cs_1001:1
  1001:1
 end-set
 !
 route-policy rt_stitch1
  if extcommunity rt matches-any cs_100:1 then
   set extcommunity rt cs_1000:1 additive
  endif
 end-policy
 !
 route-policy add_bgp_ao
  set community (accept-own) additive
 end-policy
 !
```
```
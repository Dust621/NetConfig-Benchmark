```markdown
# Peering Between BGP Routers Within a Confederation

## Table 7: Feature History Table

| Description | Release Name | Feature Name |
|------------|--------------|--------------|
| You can now enable BGP peering between routers in the sub-autonomous system (AS) within a confederation to advertise specific router updates using iBGP. This capability ensures that the mesh of routers between sub-ASes in a confederation maintains consistent routing tables, ensuring proper network reachability. Enabling this feature helps improve preventing performance reduction and traffic management challenges. | Release 7.11.1 | Peering Between BGP Routers Within the Same Confederation |

## Feature Changes

The feature introduces these changes:

### CLI

**New Command:**

- `allowconfedas-in`

### YANG Data Models

- New XPaths for:
  - `Cisco-IOS-XR-ipv4-bgp-cfg.yang`
  - `Cisco-IOS-XR-um-router-bgp-cfg`  
  *(see GitHub, YANG Data Models Navigator)*

## Overview

This feature, with its ability to enable BGP peering between routers in the sub-autonomous system (AS) within a confederation, allows for specific router updates to be advertised using iBGP. This ensures that in the mesh of routers between sub-ASes in a confederation, the routers maintain consistent routing tables and ensure proper reachability between networks within the confederation.

To enable this feature, users need to configure the `allowconfedas-in` command, thus circumventing the split horizon rule. You can specify the number of times the peer routers in the confederation can learn from each other when you configure the `allowconfedas-in` command.

In specific scenarios necessitating routing customization and optimization, breaking the split horizon rule is necessary. This rule restricts routers from sharing routes within the confederation. This feature allows you to achieve that. You can configure the `allowconfedas-in` command to permit peers to learn routes from the same confederation.

In the topology illustrated in **Figure 1: Peering Between BGP Routers Within the Same Confederation**, the PE1 router connects to the ISP router via the `192.0.2.0/24` prefix, while the PE2 router connects via the `198.51.100.0/24` prefix. The CE router advertises the `10.10.10.0/24` route to PE1, which, in turn, advertises it to PE2. To achieve this, PE1 advertises the route to the ISP router, which then passes it to PE2 since PE1 and PE2 aren't directly connected. While relaying the advertisement, the ISP router learns the route.

PE2, with a confederation AS number of AS 20, examines the AS number list in the advertisement to understand the route's path. PE2 identifies the AS numbers of the ISP router (AS 500) and PE1 router (AS 100). As the AS numbers of both PE1 and PE2 routers match, indicating they belong to the same confederation, PE2 drops the route in accordance with the split horizon rule. Hence, these routers do not learn each other's routes.

The PE1 and PE2 routers are part of the same confederation and have different AS numbers. In this case, the `allowas-in` command, which prevents dropping of the routes coming from a peer router of the same autonomous system, is not enough to allow the loop detection to be bypassed. Because of this, PE2 will not be able to learn prefixes from the PE1 router.

To override the split horizon rule and prevent PE2 from discarding the learned route, configure the `allowconfedas-in` command on both the PE1 and PE2 routers. The `allowconfedas-in` command enables you to configure the frequency with which peer routers within the same confederation learn from each other.

**Figure 2: Peering Between BGP Routers Within the Same Confederation**

## Terminology

### Autonomous Systems

BGP, operating as an Exterior Gateway Protocol (EGP), establishes loop-free interdomain routing between autonomous systems (AS). An AS comprises routers under single administration, utilizing IGPs for internal routing. Additionally, it employs EGP to route packets beyond its boundaries.

### Sub-Autonomous System

A sub-autonomous system is a distinct subset within a larger autonomous system, possessing individual administrative control. It operates with specific routing policies, contributing to the hierarchical organization and efficient management of network configurations.

### Confederation

To reduce the iBGP mesh, an autonomous system can be segmented into sub-autonomous systems organized into a confederation. Externally, this confederation appears as a single autonomous system. Internally, each autonomous system is fully meshed but maintains limited connections to others in the same confederation. Peers in different autonomous systems engage in eBGP sessions, exchanging routing information resembling iBGP peers, preserving vital parameters like next hop, MED, and local preference.

### Autonomous System Number

The Autonomous System Number (ASN) is crucial in networking, serving as a unique identifier for autonomous systems, including sub-autonomous systems within a confederation.

### Split Horizon

Split horizon, a network protocol routing rule, boosts stability by prohibiting routers in the same confederation from sharing routes. It prevents a router from advertising routes back to the network from which it learned them. This prevents potential loops, ensuring accurate network topology views and enabling efficient data forwarding, thereby addressing routing issues.

## Restrictions for Peering Between BGP Routers Within the Same Confederation

Peer routers within a confederation are restricted in the frequency at which they can exchange information with each other on configuring the `allowconfedas-in` command. The number of times they can share information ranges from 1 to 10. The default value is 3.

## Configure Peering Between BGP Routers Within the Same Confederation

### Configuration Example

To enable peering between routers that exist in the same confederation, perform the following steps:

- Enter router configuration mode.
- Assign BGP autonomous systems belonging to a confederation.
- Assign an identifier to the confederation.
- Place the router in neighbor configuration mode for routing and configure the neighbor IP address as a BGP peer.
- Specify either the IPv4 or IPv6 address family and enter address family configuration submode.
- Enable peer routers in the same confederation to learn from each other for a specified number of times.

```bash
Router# router bgp 65001
Router(config-bgp)# bgp confederation peers 65002
Router(config-bgp)# bgp confederation identifier 100
Router(config-bgp)# neighbor 198.51.100.3
Router(config-bgp-nbr)# address-family ipv4 unicast
Router(config-bgp-nbr-af)# allowconfedas-in 1
```

### Running Configuration

```bash
router bgp 65001
 bgp confederation peers 65002
 bgp confederation identifier 100
 neighbor 198.51.100.3
  address-family ipv4 unicast
   allowconfedas-in 1
```

### Verification

Verify the learning of routes among BGP peers. This output shows that the peers within the same confederation have learned from each others' routes, and the learning among peers has occurred thrice.

```bash
show bgp neighbor 198.51.100.3 | in allow
Fri Mar 7 15:38:13.092 +0530
Inbound soft reconfiguration allowed (override route-refresh)
My confederation AS number is allowed 3 times in received updates.
```
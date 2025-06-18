```markdown
# BGP Link-State

BGP Link-State (LS) is an Address Family Identifier (AFI) and Sub-address Family Identifier (SAFI) originally defined to carry interior gateway protocol (IGP) link-state information through BGP. The BGP Network Layer Reachability Information (NLRI) encoding format for BGP-LS and a new BGP Path Attribute called the BGP-LS attribute are defined in RFC7752. The identifying key of each Link-State object, namely a node, link, or prefix, is encoded in the NLRI and the properties of the object are encoded in the BGP-LS attribute.

IGPs do not use BGP LS data from remote peers. BGP does not download the received BGP LS data to any other component on the router.

## BGP-LS Applications

An example of a BGP-LS application is the Segment Routing Path Computation Element (SR-PCE). The SR-PCE can learn the SR capabilities of the nodes in the topology and the mapping of SR segments to those nodes. This can enable the SR-PCE to perform path computations based on SR-TE and to steer traffic on paths different from the underlying IGP-based distributed best-path computation.

## Deployment Scenario

The following figure shows a typical deployment scenario. In each IGP area, one or more nodes (BGP speakers) are configured with BGP-LS. These BGP speakers form an iBGP mesh by connecting to one or more route-reflectors. This way, all BGP speakers (specifically the route-reflectors) obtain Link-State information from all IGP areas (and from other ASes from eBGP peers).

## Exchange Link State Information with BGP Neighbor

The following example shows how to exchange link-state information with a BGP neighbor:

```bash
Router# configure
Router(config)# router bgp 1
Router(config-bgp)# neighbor 10.0.0.2
Router(config-bgp-nbr)# remote-as 1
Router(config-bgp-nbr)# address-family link-state link-state
Router(config-bgp-nbr-af)# exit
```

## IGP Link-State Database Distribution

A given BGP node may have connections to multiple, independent routing domains. IGP link-state database distribution into BGP-LS is supported for both OSPF and IS-IS protocols in order to distribute this information on to controllers or applications that desire to build paths spanning or including these multiple domains.

To distribute OSPFv2 link-state data using BGP-LS, use the `distribute link-state` command in router configuration mode.

```bash
Router# configure
Router(config)# router ospf 100
Router(config-ospf)# distribute link-state instance-id 32
```

## Usage Guidelines and Limitations

- BGP-LS supports IS-IS and OSPFv2.
- The identifier field of BGP-LS (referred to as the Instance-ID) identifies the IGP routing domain where the NLRI belongs. The NLRIs representing link-state objects (nodes, links, or prefixes) from the same IGP routing instance must use the same Instance-ID value.
- When there is only a single protocol instance in the network where BGP-LS is operational, we recommend configuring the Instance-ID value to 0.
- Assign consistent BGP-LS Instance-ID values on all BGP-LS Producers within a given IGP domain.
- NLRIs with different Instance-ID values are considered to be from different IGP routing instances.
- Unique Instance-ID values must be assigned to routing protocol instances operating in different IGP domains. This allows the BGP-LS Consumer (for example, SR-PCE) to build an accurate segregated multi-domain topology based on the Instance-ID values, even when the topology is advertised via BGP-LS by multiple BGP-LS Producers in the network.
- If the BGP-LS Instance-ID configuration guidelines are not followed, a BGP-LS Consumer may see duplicate link-state objects for the same node, link, or prefix when there are multiple BGP-LS Producers deployed. This may also result in the BGP-LS Consumers getting an inaccurate network-wide topology.

### Segment Routing Attributes

For segment routing, the following attributes have been added to BGP-LS:

- **Node** — Segment routing capability (including SRGB range) and algorithm
- **Link** — Adjacency SID and LAN adjacency SID
- **Prefix** — Prefix SID and segment routing mapping server (SRMS) prefix range

## Configure BGP Link-State

To exchange BGP link-state (LS) information with a BGP neighbor, perform these steps:

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family link-state link-state`
4. `neighbor ip-address`
5. `remote-as as-number`
6. `address-family link-state link-state`
7. Use the `commit` or `end` command.

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

Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** `address-family link-state link-state`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family link-state link-state
```

Distributes BGP link-state information to the specified neighbor.

**Step 4** `neighbor ip-address`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 10.0.0.2
```

Configures a CE neighbor. The `ip-address` argument must be a private address.

**Step 5** `remote-as as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 1
```

Configures the remote AS for the CE neighbor.

**Step 6** `address-family link-state link-state`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family link-state link-state
```

Distributes BGP link-state information to the specified neighbor.

**Step 7** Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Example

```bash
router bgp 100
 address-family link-state link-state
 !
 neighbor 10.0.0.2
  remote-as 1
  address-family link-state link-state
```

## Configure Domain Distinguisher

To configure unique identifier four-octet ASN, perform these steps:

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family link-state link-state`
4. `domain-distinguisher unique-id`
5. Use the `commit` or `end` command.

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

Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** `address-family link-state link-state`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family link-state link-state
```

Enters address-family link-state configuration mode.

**Step 4** `domain-distinguisher unique-id`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# domain-distinguisher 1234:1.2.3.4
```

Configures unique identifier four-octet ASN. Range is from 1 to 4294967295.

**Step 5** Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## IGP Extensions

A given BGP node may have connections to multiple, independent routing domains. IGP link state distribution into BGP has been added for both the OSPF and ISIS protocols to enable that node to likewise pass this information on to applications that desire to build paths spanning or including these multiple domains.
```
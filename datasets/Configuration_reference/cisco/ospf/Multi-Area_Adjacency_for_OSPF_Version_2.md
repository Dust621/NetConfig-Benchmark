# Multi-Area Adjacency for OSPF Version 2

The multi-area adjacency feature for OSPFv2 allows a link to be configured on the primary interface in more than one area so that the link could be considered as an intra-area link in those areas and configured as a preference over more expensive paths.

This feature establishes a point-to-point unnumbered link in an OSPF area. A point-to-point link provides a topological path for that area, and the primary adjacency uses the link to advertise the link consistent with draft-ietf-ospf-multi-area-adj-06.

## Multi-Area Interface Attributes and Limitations

The following are multi-area interface attributes and limitations:

- Exists as a logical construct over an existing primary interface for OSPF; however, the neighbor state on the primary interface is independent of the multi-area interface.
- Establishes a neighbor relationship with the corresponding multi-area interface on the neighboring router. A mixture of multi-area and primary interfaces is not supported.
- Advertises an unnumbered point-to-point link in the router link state advertisement (LSA) for the corresponding area when the neighbor state is full.
- Created as a point-to-point network type. You can configure multi-area adjacency on any interface where only two OSF speakers are attached. In the case of native broadcast networks, the interface must be configured as an OPSF point-to-point type using the network point-to-point command to enable the interface for a multi-area adjacency.
- Inherits the Bidirectional Forwarding Detection (BFD) characteristics from its primary interface. BFD is not configurable under a multi-area interface; however, it is configurable under the primary interface.

## Configure Multi-area Adjacency

This task explains how to create multiple areas on an OSPF primary interface.

### Before You Begin

You can configure multi-area adjacency on any interface where only two OSF speakers are attached. In the case of native broadcast networks, the interface must be configured as an OPSF point-to-point type using the network point-to-point command to enable the interface for a multi-area adjacency.

> **Note:** 

### SUMMARY STEPS

1. `configure`
2. `router ospf process-name`
3. `area area-id`
4. `interface type interface-path-id`
5. `area area-id`
6. `multi-area-interface type interface-path-id`
7. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1: `configure`

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2: `router ospf process-name`

```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode. The `process-name` argument is any alphanumeric string no longer than 40 characters.

> **Note:**

#### Step 3: `area area-id`

```bash
RP/0/RP0/CPU0:router(config-ospf)# area 0
```

Enters area configuration mode and configures a backbone area.

- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 4: `interface type interface-path-id`

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface Serial 0/1/0/3
```

Enters interface configuration mode and associates one or more interfaces to the area.

#### Step 5: `area area-id`

```bash
RP/0/RP0/CPU0:router(config-ospf)# area 1
```

Enters area configuration mode and configures an area used for multiple area adjacency.

- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 6: `multi-area-interface type interface-path-id`

```bash
RP/0/RP0/CPU0:router(config-ospf)# multi-area-interface Serial 0/1/0/3
```

Enables multiple adjacencies for different OSPF areas and enters multi-area interface configuration mode.

#### Step 7: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Example

The multi-area interface inherits the interface characteristics from its primary interface, but some interface characteristics can be configured under the multi-area interface configuration mode as shown below:

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# multi-area-interface TenGigE 0/0/0/0
RP/0/RP0/CPU0:router(config-ospf-ar-mif)# ?
authentication           Enable authentication
authentication-key       Authentication password (key)
cost                     Interface cost
cost-fallback            Cost when cumulative bandwidth goes below the theshold
database-filter          Filter OSPF LSA during synchronization and flooding
dead-interval            Interval after which a neighbor is declared dead
distribute-list          Filter networks in routing updates
hello-interval           Time between HELLO packets
message-digest-key       Message digest authentication password (key)
mtu-ignore               Enable/Disable ignoring of MTU in DBD packets
packet-size              Customize size of OSPF packets upto MTU
retransmit-interval      Time between retransmitting lost link state advertisements
transmit-delay           Estimated time needed to send link-state update packet
RP/0/RP0/CPU0:router(config-ospf-ar-mif)#
```
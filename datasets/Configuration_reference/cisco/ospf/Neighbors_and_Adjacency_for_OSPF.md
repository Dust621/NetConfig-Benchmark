# Neighbors and Adjacency for OSPF

Routers that share a segment (Layer 2 link between two interfaces) become neighbors on that segment. OSPF uses the hello protocol as a neighbor discovery and keep alive mechanism. The hello protocol involves receiving and periodically sending hello packets out each interface. The hello packets list all known OSPF neighbors on the interface. Routers become neighbors when they see themselves listed in the hello packet of the neighbor.

After two routers are neighbors, they may proceed to exchange and synchronize their databases, which creates an adjacency. On broadcast and NBMA networks all neighboring routers have an adjacency.

## Configure Neighbors for Nonbroadcast Networks

This task explains how to configure neighbors for a nonbroadcast network. This task is optional.

### Before you begin

Configuring NBMA networks as either broadcast or nonbroadcast assumes that there are virtual circuits from every router to every router or fully meshed network.

### SUMMARY STEPS

1. `configure`
2. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`
3. `router-id { router-id }`
4. `area area-id`
5. `network { broadcast | non-broadcast }`
6. `dead-interval seconds`
7. `hello-interval seconds`
8. `interface type interface-path-id`
9. Do one of the following:
   - `neighbor ip-address [ priority number ] [ poll-interval seconds ][ cost number ]`
   - `neighbor ipv6-link-local-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`
10. Repeat Step 9 for all neighbors on the interface.
11. `exit`
12. `interface type interface-path-id`
13. Do one of the following:
    - `neighbor ip-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`
    - `neighbor ipv6-link-local-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`
14. Repeat Step 13 for all neighbors on the interface.
15. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1

```bash
configure
```

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2

Do one of the following:
- `router ospf process-name`
- `router ospfv3 process-name`

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```

or

```bash
RP/0/RP0/CPU0:router(config)# router ospfv3 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode.

or

Enables OSPFv3 routing for the specified routing process and places the router in router ospfv3 configuration mode.

The `process-name` argument is any alphanumeric string no longer than 40 characters.

> **Note**

#### Step 3

```bash
router-id { router-id }
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# router-id 192.168.4.3
```

Configures a router ID for the OSPF process.

> **Note**  
> We recommend using a stable IP address as the router ID.

#### Step 4

```bash
area area-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# area 0
```

Enters area configuration mode and configures an area for the OSPF process.

- The example configures a backbone area.
- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 5

```bash
network { broadcast | non-broadcast }
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# network non-broadcast
```

Configures the OSPF network type to a type other than the default for a given medium.

- The example sets the network type to NBMA.

#### Step 6

```bash
dead-interval seconds
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# dead-interval 40
```

(Optional) Sets the time to wait for a hello packet from a neighbor before declaring the neighbor down.

#### Step 7

```bash
hello-interval seconds
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# hello-interval 10
```

(Optional) Specifies the interval between hello packets that OSPF sends on the interface.

#### Step 8

```bash
interface type interface-path-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface TenGigE 0/2/0/0
```

Enters interface configuration mode and associates one or more interfaces for the area configured in Step 4.

- In this example, the interface inherits the nonbroadcast network type and the hello and dead intervals from the areas because the values are not set at the interface level.

#### Step 9

Do one of the following:
- `neighbor ip-address [ priority number ] [ poll-interval seconds ][ cost number ]`
- `neighbor ipv6-link-local-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar-if)# neighbor 10.20.20.1 priority 3 poll-interval 15
```

or

```bash
RP/0/RP0/CPU0:router(config-ospf-ar-if)# neighbor fe80::3203:a0ff:fe9d:f3fe
```

Configures the IPv4 address of OSPF neighbors interconnecting to nonbroadcast networks.

or

Configures the link-local IPv6 address of OSPFv3 neighbors.

- The `ipv6-link-local-address` argument must be in the form documented in RFC 2373 in which the address is specified in hexadecimal using 16-bit values between colons.
- The `priority` keyword notifies the router that this neighbor is eligible to become a DR or BDR. The priority value should match the actual priority setting on the neighbor router. The neighbor priority default value is zero.
- Neighbors with no specific cost configured assumes the cost of the interface, based on the `cost` command.
- The `database-filter` keyword filters outgoing LSAs to an OSPF neighbor. If you specify the `all` keyword, incoming and outgoing LSAs are filtered.

#### Step 10

Repeat Step 9 for all neighbors on the interface.

---

#### Step 11

```bash
exit
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar-if)# exit
```

Enters area configuration mode.

#### Step 12

```bash
interface type interface-path-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface TenGigE 0/3/0/0
```

Enters interface configuration mode and associates one or more interfaces for the area configured in Step 4.

- In this example, the interface inherits the nonbroadcast network type and the hello and dead intervals from the areas because the values are not set at the interface level.

#### Step 13

Do one of the following:
- `neighbor ip-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`
- `neighbor ipv6-link-local-address [ priority number ] [ poll-interval seconds ][ cost number ] [ database-filter [ all ]]`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# neighbor 10.34.16.6
```

or

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# neighbor fe80::3203:a0ff:fe9d:f3f
```

Configures the IPv4 address of OSPF neighbors interconnecting to nonbroadcast networks.

or

Configures the link-local IPv6 address of OSPFv3 neighbors.

- The `ipv6-link-local-address` argument must be in the form documented in RFC 2373 in which the address is specified in hexadecimal using 16-bit values between colons.
- The `priority` keyword notifies the router that this neighbor is eligible to become a DR or BDR. The priority value should match the actual priority setting on the neighbor router. The neighbor priority default value is zero.
- Neighbors with no specific cost configured assumes the cost of the interface, based on the `cost` command.
- The `database-filter` keyword filters outgoing LSAs to an OSPF neighbor. If you specify the `all` keyword, incoming and outgoing LSAs are filtered. Use with extreme caution since filtering may cause the routing topology to be seen as entirely different between two neighbors, resulting in traffic disruption or routing loops.

#### Step 14

Repeat Step 13 for all neighbors on the interface.

---

#### Step 15

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.
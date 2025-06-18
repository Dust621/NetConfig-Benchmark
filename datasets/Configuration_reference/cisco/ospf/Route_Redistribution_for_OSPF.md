# Route Redistribution for OSPF

Redistribution allows different routing protocols to exchange routing information. This technique can be used to allow connectivity to span multiple routing protocols. It is important to remember that the redistribute command controls redistribution into an OSPF process and not from OSPF.

## Redistribute Routes into OSPF

This task redistributes routes from an IGP (could be a different OSPF process) into OSPF.

## SUMMARY STEPS

1. `configure`
2. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`
3. `router-id { router-id }`
4. `redistribute protocol [ process-id ] { level-1 | level-1-2 | level-2 } [ metric metric-value ] [ metric-type type-value ] [ match { external [ 1 | 2 ]} [ tag tag-value ] [ route-policy policy-name ]`
5. Do one of the following:
   - `summary-prefix address mask [ not-advertise ] [ tag tag ]`
   - `summary-prefix ipv6-prefix / prefix-length [ not-advertise ] [ tag tag ]`
6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1

`configure`

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2

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

**Note:**

### Step 3

`router-id { router-id }`

**Example:**

```bash
RRP/0/RP0/CPU0:router(config-ospf)# router-id 192.168.4.3
```

Configures a router ID for the OSPF process.

We recommend using a stable IPv4 address as the router ID.

**Note:**

### Step 4

`redistribute protocol [ process-id ] { level-1 | level-1-2 | level-2 } [ metric metric-value ] [ metric-type type-value ] [ match { external [ 1 | 2 ]} [ tag tag-value ] [ route-policy policy-name ]`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# redistribute bgp 100
```

or

```bash
RP/0/RP0/CPU0:router(config-router)# redistribute bgp 110
```

Redistributes OSPF routes from one routing domain to another routing domain.

or

Redistributes OSPFv3 routes from one routing domain to another routing domain.

- This command causes the router to become an ASBR by definition.
- OSPF tags all routes learned through redistribution as external.
- The protocol and its process ID, if it has one, indicate the protocol being redistributed into OSPF.
- The metric is the cost you assign to the external route. The default is 20 for all protocols except BGP, whose default metric is 1.
- The OSPF example redistributes BGP autonomous system 1, Level 1 routes into OSPF as Type 2 external routes.
- The OSPFv3 example redistributes BGP autonomous system 1, Level 1 and 2 routes into OSPF. The external link type associated with the default route advertised into the OSPFv3 routing domain is the Type 1 external route.

**Note:** RPL is not supported for OSPFv3.

### Step 5

Do one of the following:
- `summary-prefix address mask [ not-advertise ] [ tag tag ]`
- `summary-prefix ipv6-prefix / prefix-length [ not-advertise ] [ tag tag ]`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# summary-prefix 10.1.0.0 255.255.0.0
```

or

```bash
RP/0/RP0/CPU0:router(config-router)# summary-prefix 2010:11:22::/32
```

(Optional) Creates aggregate addresses for OSPF.

or

(Optional) Creates aggregate addresses for OSPFv3.

- This command provides external route summarization of the non-OSPF routes.
- External ranges that are being summarized should be contiguous. Summarization of overlapping ranges from two different routers could cause packets to be sent to the wrong destination.
- This command is optional. If you do not specify it, each route is included in the link-state database and advertised in LSAs.
- In the OSPFv2 example, the summary address 10.1.0.0 includes address 10.1.1.0, 10.1.2.0, 10.1.3.0, and so on. Only the address 10.1.0.0 is advertised in an external LSA.
- In the OSPFv3 example, the summary address 2010:11:22::/32 has addresses such as 2010:11:22:0:1000::1, 2010:11:22:0:2000:679:1, and so on. Only the address 2010:11:22::/32 is advertised in the external LSA.

### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

## Example

The following example uses prefix lists to limit the routes redistributed from other protocols. Only routes with 9898:1000 in the upper 32 bits and with prefix lengths from 32 to 64 are redistributed from BGP 42. Only routes not matching this pattern are redistributed from BGP 1956.

```bash
ipv6 prefix-list list1
seq 10 permit 9898:1000::/32 ge 32 le 64
ipv6 prefix-list list2
seq 10 deny 9898:1000::/32 ge 32 le 64
seq 20 permit ::/0 le 128
router ospfv3 1
router-id 10.0.0.217
redistribute bgp 42
redistribute bgp 1956
distribute-list prefix-list list1 out bgp 42
distribute-list prefix-list list2 out bgp 1956
area 1
interface TenGigE 0/2/0/0
```
# Summarize Subnetwork LSAs on OSPF ABR

If you configured two or more subnetworks when you assigned your IP addresses to your interfaces, you might want the software to summarize (aggregate) into a single LSA all of the subnetworks that the local area advertises to another area. Such summarization would reduce the number of LSAs and thereby conserve network resources. This summarization is known as interarea route summarization. It applies to routes from within the autonomous system. It does not apply to external routes injected into OSPF by way of redistribution.

This task configures OSPF to summarize subnetworks into one LSA, by specifying that all subnetworks that fall into a range are advertised together. This task is performed on an ABR only.

## SUMMARY STEPS

1. `configure`

2. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`

3. `router-id { router-id }`

4. `area area-id`

5. Do one of the following:
   - `range ip-address mask [ advertise | not-advertise ]`
   - `range ipv6-prefix / prefix-length [ advertise | not-advertise ]`

6. `interface type interface-path-id`

7. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1

```bash
configure
```

**Example**:
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

---

### Step 2

Do one of the following:
- `router ospf process-name`
- `router ospfv3 process-name`

**Example**:
```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```
or
```bash
RP/0/RP0/CPU0:router(config)# router ospfv3 1
```

- Enables OSPF routing for the specified routing process and places the router in router configuration mode.
- Enables OSPFv3 routing for the specified routing process and places the router in router ospfv3 configuration mode.

**Note**:  
The `process-name` argument is any alphanumeric string no longer than 40 characters.

---

### Step 3

```bash
router-id { router-id }
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-ospf)# router-id 192.168.4.3
```

Configures a router ID for the OSPF process.

**Note**:  
We recommend using a stable IPv4 address as the router ID.

---

### Step 4

```bash
area area-id
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-ospf)# area
```

Enters area configuration mode and configures a nonbackbone area for the OSPF process.

- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

---

### Step 5

Do one of the following:
- `range ip-address mask [ advertise | not-advertise ]`
- `range ipv6-prefix / prefix-length [ advertise | not-advertise ]`

**Example**:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# range 192.168.0.0 255.255.0.0 advertise
```
or
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# range 4004:f000::/32 advertise
```

Consolidates and summarizes OSPF routes at an area boundary.

- The `advertise` keyword causes the software to advertise the address range of subnetworks in a Type 3 summary LSA.
- The `not-advertise` keyword causes the software to suppress the Type 3 summary LSA, and the subnetworks in the range remain hidden from other areas.
- In the first example, all subnetworks for network `192.168.0.0` are summarized and advertised by the ABR into areas outside the backbone.
- In the second example, two or more IPv4 interfaces are covered by a `192.x.x` network.

---

### Step 6

```bash
interface type interface-path-id
```

**Example**:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface TenGigE 0/0/0/0
```

Enters interface configuration mode and associates one or more interfaces to the area.

---

### Step 7

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

## Example

The following example shows the prefix range `2300::/16` summarized from area 1 into the backbone:

```bash
router ospfv3 1
router-id 192.168.0.217
area 0
interface TenGigE 0/0/0/0
area 1
range 2300::/16
interface TenGigE 0/0/0/0
```
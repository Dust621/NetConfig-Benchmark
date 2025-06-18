# Virtual Link and Transit Area for OSPF

In OSPF, routing information from all areas is first summarized to the backbone area by ABRs. The same ABRs, in turn, propagate such received information to their attached areas. Such hierarchical distribution of routing information requires that all areas be connected to the backbone area (Area 0). 

Occasions might exist for which an area must be defined, but it cannot be physically connected to Area 0. Examples of such an occasion might be if your company makes a new acquisition that includes an OSPF area, or if Area 0 itself is partitioned.

In the case in which an area cannot be connected to Area 0, you must configure a virtual link between that area and Area 0. The two endpoints of a virtual link are ABRs, and the virtual link must be configured in both routers. The common nonbackbone area to which the two routers belong is called a transit area. A virtual link specifies the transit area and the router ID of the other virtual endpoint (the other ABR).

**Note:** A virtual link cannot be configured through a stub area or NSSA.

## Figure 1: Virtual Link to Area 0

This figure illustrates a virtual link from Area 3 to Area 0.

## Create Virtual Link

This task explains how to create a virtual link to your backbone (area 0) and apply MD5 authentication. You must perform the steps described on both ABRs, one at each end of the virtual link.

After you explicitly configure area parameter values, they are inherited by all interfaces bound to that area—unless you override the values and configure them explicitly for the interface.

### Before you begin

The following prerequisites must be met before creating a virtual link with MD5 authentication to area 0:

- You must have the router ID of the neighbor router at the opposite end of the link to configure the local router. You can execute the `show ospf` or `show ospfv3` command on the remote router to get its router ID.
- For a virtual link to be successful, you need a stable router ID at each end of the virtual link. You do not want them to be subject to change, which could happen if they are assigned by default. Therefore, we recommend that you perform one of the following tasks before configuring a virtual link:
  - Use the `router-id` command to set the router ID. This strategy is preferable.
  - Configure a loopback interface so that the router has a stable router ID.
- Before configuring your virtual link for OSPF Version 2, you must decide whether to configure plain text authentication, MD5 authentication, or no authentication (which is the default). Your decision determines whether you need to perform additional tasks related to authentication.

## SUMMARY STEPS

1. Do one of the following:
   - `show ospf [ process-name ]`
   - `show ospfv3 [ process-name ]`

2. `configure`

3. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`

4. `router-id { router-id }`

5. `area area-id`

6. `virtual-link router-id`

7. `authentication message-digest`

8. `message-digest-key key-id md5 { key | clear key | encrypted key }`

9. Repeat all of the steps in this task on the ABR that is at the other end of the virtual link. Specify the same key ID and key that you specified for the virtual link on this router.

10. Use the `commit` or `end` command.

11. Do one of the following:
    - `show ospf [ process-name ] [ area-id ] virtual-links`
    - `show ospfv3 [ process-name ] virtual-links`

## DETAILED STEPS

### Step 1

Do one of the following:
- `show ospf [ process-name ]`
- `show ospfv3 [ process-name ]`

**Example:**
```bash
RP/0//CPU0:router# show ospf
```
or
```bash
RP/0//CPU0:router# show ospfv3
```

(Optional) Displays general information about OSPF routing processes.

- The output displays the router ID of the local router. You need this router ID to configure the other end of the link.

### Step 2

`configure`

**Example:**
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 3

Do one of the following:
- `router ospf process-name`
- `router ospfv3 process-name`

**Example:**
```bash
RP/0//CPU0:router(config)# router ospf 1
```
or
```bash
RP/0//CPU0:router(config)# router ospfv3 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode.

or

Enables OSPFv3 routing for the specified routing process and places the router in router ospfv3 configuration mode.

The `process-name` argument is any alphanumeric string no longer than 40 characters.

### Step 4

`router-id { router-id }`

**Example:**
```bash
RP/0//CPU0:router(config-ospf)# router-id 192.168.4.3
```

Configures a router ID for the OSPF process.

We recommend using a stable IPv4 address as the router ID.

### Step 5

`area area-id`

**Example:**
```bash
RP/0//CPU0:router(config-ospf)# area 1
```

Enters area configuration mode and configures a nonbackbone area for the OSPF process.

- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

### Step 6

`virtual-link router-id`

**Example:**
```bash
RP/0//CPU0:router(config-ospf-ar)# virtual-link 10.3.4.5
```

Defines an OSPF virtual link.

### Step 7

`authentication message-digest`

**Example:**
```bash
RP/0//CPU0:router(config-ospf-ar-vl)# authentication message-digest
```

Selects MD5 authentication for this virtual link.

### Step 8

`message-digest-key key-id md5 { key | clear key | encrypted key }`

**Example:**
```bash
RP/0//CPU0:router(config-ospf-ar-vl)# message-digest-key 4 md5 yourkey
```

Defines an OSPF virtual link.

- The `key-id` argument is a number in the range from 1 to 255. The `key` argument is an alphanumeric string of up to 16 characters. The routers at both ends of the virtual link must have the same key identifier and key to be able to route OSPF traffic.
- The `authentication-key key` command is not supported for OSPFv3.
- Once the key is encrypted it must remain encrypted.

### Step 9

Repeat all of the steps in this task on the ABR that is at the other end of the virtual link. Specify the same key ID and key that you specified for the virtual link on this router.

### Step 10

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

### Step 11

Do one of the following:
- `show ospf [ process-name ] [ area-id ] virtual-links`
- `show ospfv3 [ process-name ] virtual-links`

**Example:**
```bash
RP/0//CPU0:router# show ospf 1 2 virtual-links
```
or
```bash
RP/0//CPU0:router# show ospfv3 1 virtual-links
```

(Optional) Displays the parameters and the current state of OSPF virtual links.

## Creating Virtual Link - Example

### ABR 1 Configuration

### ABR 2 Configuration

In the following example, the `show ospfv3 virtual links` command verifies that the OSPF_VL0 virtual link to the OSPFv3 neighbor is up, the ID of the virtual link interface is 2, and the IPv6 address of the virtual link endpoint is `2003:3000::1`.

```bash
show ospfv3 virtual-links
Virtual Links for OSPFv3 1
Virtual Link OSPF_VL0 to router 10.0.0.3 is up
Interface ID 2, IPv6 address 2003:3000::1
Run as demand circuit
DoNotAge LSA allowed.
Transit area 0.1.20.255, via interface TenGigE 0/1/0/1 Cost of using 2
Transmit Delay is 5 sec,
Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
Hello due in 00:00:02
Adjacency State FULL (Hello suppressed)
Index 0/2/3, retransmission queue length 0, number of retransmission 1
First 0(0)/0(0)/0(0) Next 0(0)/0(0)/0(0)
Last retransmission scan length is 1, maximum is 1
Last retransmission scan time is 0 msec, maximum is 0 msec
```

**Check for lines:**
- `Virtual Link OSPF_VL0 to router 10.0.0.3 is up`
- `Adjacency State FULL (Hello suppressed)`

State is up and Adjacency State is FULL.

This example shows how to set up a virtual link to connect the backbone through area 1 for the OSPFv3 topology that consists of areas 0 and 1 and virtual links `10.0.0.217` and `10.0.0.212`:

**ABR 1 Configuration:**
```bash
router ospfv3 1
router-id 10.0.0.217
area 0
interface TenGigE 0/2/0/1
area 1
virtual-link 10.0.0.212
interface TenGigE 0/2/0/0
```

**ABR 2 Configuration:**
```bash
router ospfv3 1
router-id 10.0.0.212
area 0
interface TenGigE 0/3/0/1
area 1
virtual-link 10.0.0.217
interface TenGigE 0/2/0/0
```

In this example, all interfaces on router ABR1 use MD5 authentication:

```bash
router ospf ABR1
router-id 10.10.10.10
authentication message-digest
message-digest-key 100 md5 0 cisco
area 0
interface TenGigE 0/2/0/1
interface TenGigE 0/3/0/0
area 1
interface TenGigE 0/2/0/0
virtual-link 10.10.5.5
```

In this example, only area 1 interfaces on router ABR3 use MD5 authentication:

```bash
router ospf ABR2
router-id 10.10.5.5
area 0
area 1
authentication message-digest
message-digest-key 100 md5 0 cisco
interface TenGigE 0/9/0/1
virtual-link 10.10.10.10
area 3
interface Loopback 0
interface TenGigE 0/9/0/0
```
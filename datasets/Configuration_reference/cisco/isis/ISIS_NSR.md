```markdown
# ISIS NSR

Non Stop Routing (NSR) suppresses IS-IS routing changes for devices with redundant route processors during processor switchover events (RP failover or ISSU), reducing network instability and downtime. When Non Stop Routing is used, switching from the active to standby RP have no impact on the other IS-IS routers in the network. All information needed to continue the routing protocol peering state is transferred to the standby processor prior to the switchover, so it can continue immediately upon a switchover.

To preserve routing across process restarts, NSF must be configured in addition to NSR.

## Configuring ISIS-NSR

### Step 1

```bash
configure
```

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2

```bash
router isis instance-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router isis 1
```

Enables IS-IS routing for the specified routing instance, and places the router in router configuration mode.

### Step 3

```bash
nsr
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis)# nsr
```

Configures the NSR feature.

### Step 4

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Step 5

```bash
show isis nsr adjacency
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show isis nsr adjacency
System Id Interface SNPA State Hold Changed NSF IPv4 BFD IPv6 BFD
R1-v1S Nii0 *PtoP* Up 83 00:00:33 Yes None None
```

Displays adjacency information.

### Step 6

```bash
show isis nsr status
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show isis nsr status
IS-IS test NSR(v1a) STATUS (HA Ready):
V1 Standby V2 Active V2 Standby
SYNC STATUS: TRUE FALSE(0) FALSE(0)
PEER CHG COUNT: 1 0 0
UP TIME: 00:03:12 not up not up
```

Displays the NSR status information.

### Step 7

```bash
show isis nsr statistics
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show isis nsr statistics
IS-IS test NSR(v1a) MANDATORY STATS :
V1 Active V1 Standby V2 Active V2 Standby
L1 ADJ: 0 0 0 0
L2 ADJ: 2 2 0 0
LIVE INTERFACE: 4 4 0 0
PTP INTERFACE: 1 1 0 0
LAN INTERFACE: 2 2 0 0
LOOPBACK INTERFACE: 1 1 0 0
TE Tunnel: 1 1 0 0
TE LINK: 2 2 0 0

NSR OPTIONAL STATS :
L1 LSP: 0 0 0 0
L2 LSP: 4 4 0 0
IPV4 ROUTES: 3 3 0 0
IPV6 ROUTES: 4 4 0 0
```

Shows number of ISIS adjacencies, lsps, routes, tunnels, Te links on active and standby routers.
```
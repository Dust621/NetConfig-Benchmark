# Label Distribution Protocol IGP Auto-configuration for OSPF

Label Distribution Protocol (LDP) Interior Gateway Protocol (IGP) auto-configuration simplifies the procedure to enable LDP on a set of interfaces used by an IGP instance, such as OSPF. LDP IGP auto-configuration can be used on a large number of interfaces (for example, when LDP is used for transport in the core) and on multiple OSPF instances simultaneously.

This feature supports the IPv4 unicast address family for the default VPN routing and forwarding (VRF) instance.

LDP IGP auto-configuration can also be explicitly disabled on an individual interface basis under LDP using the `igp auto-config disable` command. This allows LDP to receive all OSPF interfaces minus the ones explicitly disabled.

## Configure Label Distribution Protocol IGP Auto-configuration for OSPF

This task explains how to configure LDP auto-configuration for an OSPF instance. Optionally, you can configure this feature for an area of an OSPF instance.

### SUMMARY STEPS

1. `configure`
2. `router ospf process-name`
3. `mpls ldp auto-config`
4. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1

```bash
configure
```

Example:
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2

```bash
router ospf process-name
```

Example:
```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode. The `process-name` argument is any alphanumeric string no longer than 40 characters.

> **Note**

#### Step 3

```bash
mpls ldp auto-config
```

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# mpls ldp auto-config
```

Enables LDP IGP interface auto-configuration for an OSPF instance.

- Optionally, this command can be configured for an area of an OSPF instance.

#### Step 4

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Configure LDP IGP Synchronization: OSPF

Perform this task to configure LDP IGP Synchronization under OSPF. By default, there is no synchronization between LDP and IGPs.

> **Note**

### SUMMARY STEPS

1. `configure`
2. `router ospf process-name`
3. (Optional) `vrf vrf-name`
4. Use one of the following commands:
   - `mpls ldp sync`
   - `area area-id mpls ldp sync`
   - `area area-id interface name mpls ldp sync`
5. (Optional) Use one of the following commands:
   - `mpls ldp sync`
   - `area area-id mpls ldp sync`
   - `area area-id interface name mpls ldp sync`
6. Use the `commit` or `end` command.
7. (Optional) `show mpls ldp vrf vrf-name ipv4 igp sync`
8. (Optional) `show mpls ldp vrf all ipv4 igp sync`
9. (Optional) `show mpls ldp { ipv4 | ipv6 } igp sync`

### DETAILED STEPS

#### Step 1

```bash
configure
```

Example:
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2

```bash
router ospf process-name
```

Example:
```bash
RP/0/RP0/CPU0:router(config)# router ospf 100
```

Identifies the OSPF routing process and enters OSPF configuration mode.

#### Step 3

(Optional) 
```bash
vrf vrf-name
```

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# vrf red
```

Specifies the non-default VRF.

#### Step 4

Use one of the following commands:

- `mpls ldp sync`
- `area area-id mpls ldp sync`
- `area area-id interface name mpls ldp sync`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# mpls ldp sync
```

Enables LDP IGP synchronization on an interface.

#### Step 5

(Optional) Use one of the following commands:

- `mpls ldp sync`
- `area area-id mpls ldp sync`
- `area area-id interface name mpls ldp sync`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf-vrf)# mpls ldp sync
RP/0/RP0/CPU0:router(config-ospf-vrf)# area 1 mpls ldp sync
```

Enables LDP IGP synchronization on an interface for the specified VRF.

#### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

#### Step 7

(Optional) 
```bash
show mpls ldp vrf vrf-name ipv4 igp sync
```

Example:
```bash
RP/0/RP0/CPU0:router# show mpls ldp vrf red ipv4 igp sync
```

Displays the LDP IGP synchronization information for the specified VRF for address family IPv4.

#### Step 8

(Optional) 
```bash
show mpls ldp vrf all ipv4 igp sync
```

Example:
```bash
RP/0/RP0/CPU0:router# show mpls ldp vrf all ipv4 igp sync
```

Displays the LDP IGP synchronization information for all VRFs for address family IPv4.

#### Step 9

(Optional) 
```bash
show mpls ldp { ipv4 | ipv6 } igp sync
```

Example:
```bash
RP/0/RP0/CPU0:router# show mpls ldp ipv4 igp sync
RP/0/RP0/CPU0:router# show mpls ldp ipv6 igp sync
```

Displays the LDP IGP synchronization information for IPv4 or IPv6 address families.

### Example

The example shows how to configure LDP IGP synchronization for OSPF.

```bash
router ospf 100
mpls ldp sync
!
mpls ldp
igp sync delay 30
!
```
# Configure Static Route

Static routes are entirely user configurable and can point to a next-hop interface, next-hop IP address, or both. 

In the software, if an interface was specified, then the static route is installed in the Routing Information Base (RIB) if the interface is reachable. If an interface was not specified, the route is installed if the next-hop address is reachable. The only exception to this configuration is when a static route is configured with the permanent attribute, in which case it is installed in RIB regardless of reachability.

## SUMMARY STEPS

1. `configure`
2. `router static`
3. `vrf vrf-name`
4. `address-family { ipv4 | ipv6 } { unicast | multicast }`
5. `prefix mask [vrf vrf-name ] { ip-address | interface-type interface-instance } [ distance ] [ description text ] [ tag tag ] [ permanent ]`
6. Use the `commit` or `end` command.

## DETAILED STEPS

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
router static
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config)# router static
```

Enters static route configuration mode.

### Step 3

```bash
vrf vrf-name
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-static)# vrf vrf_A
```

(Optional) Enters VRF configuration mode.  
If a VRF is not specified, the static route is configured under the default VRF.

### Step 4

```bash
address-family { ipv4 | ipv6 } { unicast | multicast }
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-static-vrf)# address-family ipv4 unicast
```

Enters address family mode.

### Step 5

```bash
prefix mask [vrf vrf-name ] { ip-address | interface-type interface-instance } [ distance ] [ description text ] [ tag tag ] [ permanent ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-static-vrf-afi)# 10.0.0.0/8 172.20.16.6 110
```

Configures an administrative distance of 110.

- This example shows how to route packets for network `10.0.0.0` through to a next hop at `172.20.16.6` if dynamic information with administrative distance less than 110 is not available.

### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Default Static Route Example

A default static route is often used in simple router topologies. In the following example, a route is configured with an administrative distance of 110.

```bash
configure
router static
address-family ipv4 unicast
0.0.0.0/0 2.6.0.1 110
end
```
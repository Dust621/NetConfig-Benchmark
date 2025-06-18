```markdown
# Customize Routes for IS-IS

This task explains how to perform route functions that include injecting default routes into your IS-IS routing domain and redistributing routes learned in another IS-IS instance. This task is optional.

## SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `set-overload-bit [ on-startup { delay | wait-for-bgp }] [ level { 1 | 2 }]`
4. `address-family { ipv4 | ipv6 } [ unicast ]`
5. `default-information originate [ route-policy route-policy-name ]`
6. `redistribute isis instance [ level-1 | level-2 | level-1-2 ] [ metric metric ] [ metric-type { internal | external }] [ policy policy-name ]`
7. Do one of the following:
   - `summary-prefix address / prefix-length [ level { 1 | 2 }]`
   - `summary-prefix ipv6-prefix / prefix-length [ level { 1 | 2 }]`
8. `maximum-paths route-number`
9. `distance weight [ address / prefix-length [ route-list-name ]]`
10. `set-attached-bit`
11. Use the `commit` or `end` command.

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
router isis instance-id
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```

Enables IS-IS routing for the specified routing process, and places the router in router configuration mode.

- By default, all IS-IS instances are automatically Level 1 and Level 2. You can change the level of routing to be performed by a particular routing instance by using the `is-type` command.

### Step 3

```bash
set-overload-bit [ on-startup { delay | wait-for-bgp }] [ level { 1 | 2 }]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis)# set-overload-bit
```

(Optional) Sets the overload bit.

The configured overload bit behavior does not apply to NSF restarts because the NSF restart does not set the overload bit during restart.

> **Note:**  
> The overload bit behavior is specific to normal restarts.

### Step 4

```bash
address-family { ipv4 | ipv6 } [ unicast ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis)# address-family ipv4 unicast
```

Specifies the IPv4 or IPv6 address family, and enters router address family configuration mode.

### Step 5

```bash
default-information originate [ route-policy route-policy-name ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# default-information originate
```

(Optional) Injects a default IPv4 or IPv6 route into an IS-IS routing domain.

- The `route-policy` keyword and `route-policy-name` argument specify the conditions under which the IPv4 or IPv6 default route is advertised.
- If the `route-policy` keyword is omitted, then the IPv4 or IPv6 default route is unconditionally advertised at Level 2.

### Step 6

```bash
redistribute isis instance [ level-1 | level-2 | level-1-2 ] [ metric metric ] [ metric-type { internal | external }] [ policy policy-name ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# redistribute isis 2 level-1
```

(Optional) Redistributes routes from one IS-IS instance into another instance.

- In this example, an IS-IS instance redistributes Level 1 routes from another IS-IS instance.

### Step 7

Do one of the following:

- `summary-prefix address / prefix-length [ level { 1 | 2 }]`
- `summary-prefix ipv6-prefix / prefix-length [ level { 1 | 2 }]`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# summary-prefix 10.1.0.0/16 level 1
```
or
```bash
RP/0/RP0/CPU0:router(config-isis-af)# summary-prefix 3003:xxxx::/24 level 1
```

(Optional) Allows a Level 1-2 router to summarize Level 1 IPv4 and IPv6 prefixes at Level 2, instead of advertising the Level 1 prefixes directly when the router advertises the summary.

- This example specifies an IPv4 address and mask.
- This example specifies an IPv6 prefix, and the command must be in the form documented in RFC 2373 in which the address is specified in hexadecimal using 16-bit values between colons.
- Note that IPv6 prefixes must be configured only in the IPv6 router address family configuration submode, and IPv4 prefixes in the IPv4 router address family configuration submode.

### Step 8

```bash
maximum-paths route-number
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# maximum-paths 16
```

(Optional) Configures the maximum number of parallel paths allowed in a routing table.

### Step 9

```bash
distance weight [ address / prefix-length [ route-list-name ]]
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# distance 90
```

(Optional) Defines the administrative distance assigned to routes discovered by the IS-IS protocol.

- A different administrative distance may be applied for IPv4 and IPv6.

### Step 10

```bash
set-attached-bit
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis-af)# set-attached-bit
```

(Optional) Configures an IS-IS instance with an attached bit in the Level 1 LSP.

### Step 11

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Redistributing IS-IS Routes Between Multiple Instances: Example

The following example shows usage of the `set-attached-bit` and `redistribute` commands. Two instances, instance “1” restricted to Level 1 and instance “2” restricted to Level 2, are configured. The Level 1 instance is propagating routes to the Level 2 instance using redistribution. Note that the administrative distance is explicitly configured higher on the Level 2 instance to ensure that Level 1 routes are preferred.

Attached bit is being set for the Level 1 instance since it is redistributing routes into the Level 2 instance. Therefore, instance “1” is a suitable candidate to get from the area to the backbone.

```bash
router isis 1
 is-type level-2-only
 net 49.0001.0001.0001.0001.00
 address-family ipv4 unicast
  distance 116
  redistribute isis 2 level 2
 !
 interface HundredGigE 0/3/0/0
  address-family ipv4 unicast
 !
!
router isis 2
 is-type level-1
 net 49.0002.0001.0001.0002.00
 address-family ipv4 unicast
  set-attached-bit
 !
 interface HundredGigE 0/1/0/0
  address-family ipv4 unicast
```
```
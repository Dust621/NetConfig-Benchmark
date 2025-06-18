# Change Maximum Number of Allowable Static Routes

This task explains how to change the maximum number of allowable static routes.

## Before you begin

The number of static routes that can be configured on a router for a given address family is limited by default to 4000. The limit can be raised or lowered using the `maximum path` command. 

Note that if you use the `maximum path` command to reduce the configured maximum allowed number of static routes for a given address family below the number of static routes currently configured, the change is rejected. 

In addition, understand the following behavior: If you commit a batch of routes that would, when grouped, push the number of static routes configured above the maximum allowed, the first `n` routes in the batch are accepted. The number previously configured is accepted, and the remainder are rejected. The `n` argument is the difference between the maximum number allowed and number previously configured.

## SUMMARY STEPS

1. `configure`
2. `router static`
3. `maximum path { ipv4 | ipv6 } value`
4. Use the `commit` or `end` command.

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
maximum path { ipv4 | ipv6 } value
```

**Example:**
```bash
RP/0/RP0/CPU0:router(config-static)# maximum path ipv4 10000
```

Changes the maximum number of allowable static routes.

- Specify IPv4 or IPv6 address prefixes.
- Specify the maximum number of static routes for the given address family. The range is from 1 to 140000.
- This example sets the maximum number of static IPv4 routes to 10000.

### Step 4

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

## Additional Notes

Configuring a static route to point at interface `null 0` may be used for discarding traffic to a particular prefix. For example, if it is required to discard all traffic to prefix `2001:0DB8:42:1/64`, the following static route would be defined:

```bash
configure
router static
address-family ipv6 unicast
2001:0DB8:42:1::/64 null 0
end
```
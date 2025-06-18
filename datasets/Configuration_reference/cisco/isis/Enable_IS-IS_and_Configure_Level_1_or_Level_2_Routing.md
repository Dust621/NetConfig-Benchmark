```markdown
# Enable IS-IS and Configure Level 1 or Level 2 Routing

This task explains how to enable IS-IS and configure the routing level for an area. Configuring the routing level in Step 4 is optional, but is highly recommended to establish the proper level of adjacencies.

## Note

Users can configure the `no max-metric` command only with levels 1 or 2, that is, `no max-metric level {1|2}` in order to view the result in the output of the `show configuration` command. Else, the maximum metric configuration is not displayed in the output. This behavior is observed before committing the configuration to the router.

**Note:** Although you can configure IS-IS before you configure an IP address, no IS-IS routing occurs until at least one IP address is configured.

## SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `net network-entity-title`
4. `is-type { level-1 | level-1-2 | level-2-only }`
5. Use the `commit` or `end` command.
6. `show isis [ instance instance-id ] protocol`

## DETAILED STEPS

### Step 1: `configure`

**Example:**
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: `router isis instance-id`

**Example:**
```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```

Enables IS-IS routing for the specified routing instance, and places the router in router configuration mode.

- By default, all IS-IS instances are automatically Level 1 and Level 2. You can change the level of routing to be performed by a particular routing instance by using the `is-type` router configuration command.

### Step 3: `net network-entity-title`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis)# net 47.0004.004d.0001.0001.0c11.1110.00
```

Configures network entity titles (NETs) for the routing instance.

- Specify a NET for each routing instance if you are configuring multi-instance IS-IS.
- This example configures a router with area ID `47.0004.004d.0001` and system ID `0001.0c11.1110.00`.
- To specify more than one area address, specify additional NETs. Although the area address portion of the NET differs, the systemID portion of the NET must match exactly for all of the configured items.

### Step 4: `is-type { level-1 | level-1-2 | level-2-only }`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-isis)# is-type level-2-only
```

(Optional) Configures the system type (area or backbone router).

- By default, every IS-IS instance acts as a `level-1-2` router.
- The `level-1` keyword configures the software to perform Level 1 (intra-area) routing only. Only Level 1 adjacencies are established. The software learns about destinations inside its area only. Any packets containing destinations outside the area are sent to the nearest `level-1-2` router in the area.
- The `level-2-only` keyword configures the software to perform Level 2 (backbone) routing only, and the router establishes only Level 2 adjacencies, either with other Level 2-only routers or with `level-1-2` routers.
- The `level-1-2` keyword configures the software to perform both Level 1 and Level 2 routing. Both Level 1 and Level 2 adjacencies are established. The router acts as a border router between the Level 2 backbone and its Level 1 area.

### Step 5: Use the `commit` or `end` command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Step 6: `show isis [ instance instance-id ] protocol`

**Example:**
```bash
RP/0/RP0/CPU0:router# show isis protocol
```

(Optional) Displays summary information about the IS-IS instance.
```
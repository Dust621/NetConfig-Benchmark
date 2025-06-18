```markdown
# Configure MED Metric for BGP

Perform this task to set the multi exit discriminator (MED) to advertise to peers for routes that do not already have a metric set (routes that were received with no MED attribute).

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `default-metric value`
4. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters global configuration mode.

### Step 2: `router bgp as-number`

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: `default-metric value`

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# default-metric
```

Sets the default metric, which is used to set the MED to advertise to peers for routes that do not already have a metric set (routes that were received with no MED attribute).

### Step 4: Use the `commit` or `end` command.

- **`commit`** — Saves the configuration changes and remains within the configuration session.  
- **`end`** — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  
```
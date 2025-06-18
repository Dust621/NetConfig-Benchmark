```markdown
# Change BGP Default Local Preference Value

Perform this task to set the default local preference value for BGP paths.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `bgp default local-preference value`
4. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters global configuration mode.

### Step 2: router bgp as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: bgp default local-preference value

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp default local-preference 200
```

Sets the default local preference value from the default of 100, making it either a more preferable path (over 100) or less preferable path (under 100).

### Step 4: Use the commit or end command

- **`commit`** — Saves the configuration changes and remains within the configuration session.
  
- **`end`** — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
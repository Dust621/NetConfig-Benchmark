```markdown
# Redistribute iBGP Routes into IGP

Perform this task to redistribute iBGP routes into an Interior Gateway Protocol (IGP), such as Intermediate System-to-Intermediate System (IS-IS) or Open Shortest Path First (OSPF).

Use of the `bgp redistribute-internal` command requires the `clear route *` command to be issued to reinstall all BGP routes into the IP routing table.

> **Note**  
> Redistributing iBGP routes into IGPs may cause routing loops to form within an autonomous system. Use this command with caution.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `bgp redistribute-internal`
4. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters configuration mode.

### Step 2: router bgp as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: bgp redistribute-internal

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp redistribute-internal
```

Allows the redistribution of iBGP routes into an IGP, such as IS-IS or OSPF.

### Step 4: Use the commit or end command

- **commit** — Saves the configuration changes and remains within the configuration session.
- **end** — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```
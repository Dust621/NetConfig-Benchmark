```markdown
# Disable RIB Next-hop Dampening

Perform this task to disable RIB next-hop dampening.

## SUMMARY STEPS

1. `router rib`
2. `address-family { ipv4 | ipv6 } next-hop dampening disable`
3. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1

```bash
router rib
```

**Example:**

```bash
RP/0/RP0/CPU0:router# router rib
```

Enters RIB configuration mode.

### Step 2

```bash
address-family { ipv4 | ipv6 } next-hop dampening disable
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-rib)# address-family ipv4 next-hop dampening disable
```

Disables next-hop dampening for IPv4 address families.

### Step 3

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Output of `show route next-hop` Command: Example

The following is sample output from the `show route resolving-next-hop` command:

```bash
show route resolving-next-hop 10.0.0.1
Nexthop matches 0.0.0.0/0
Known via "static", distance 200, metric 0, candidate default path
Installed Aug 18 00:59:04.448
Directly connected nexthops
172.29.52.1, via MgmtEth0/CPU0/0
Route metric is 0
```
```
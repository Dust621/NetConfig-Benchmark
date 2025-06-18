```markdown
# Enable RCC and LCC Background Scan

Perform this task to run a background scan for Route Consistency Checker (RCC) and Label Consistency Checker (LCC).

## SUMMARY STEPS

1. `configure`
2. Use one of these commands:
   - `rcc {ipv4 | ipv6} unicast {enable | period milliseconds}`
   - `lcc {ipv4 | ipv6} unicast {enable | period milliseconds}`
3. Use the `commit` or `end` command.
4. Use one of these commands:
   - `show rcc {ipv4 | ipv6} unicast [summary | scan-id scan-id-value]`
   - `show lcc {ipv4 | ipv6} unicast [summary | scan-id scan-id-value]`

## DETAILED STEPS

### Step 1: `configure`

**Example:**
```bash
RP/0/RP0/CPU0:router# configure
```
Enters configuration mode.

### Step 2: Use RCC or LCC Commands

Use one of these commands:
- `rcc {ipv4 | ipv6} unicast {enable | period milliseconds}`
- `lcc {ipv4 | ipv6} unicast {enable | period milliseconds}`

**Example:**
```bash
RP/0/RP0/CPU0:router(config)# rcc ipv6 unicast enable
RP/0/RP0/CPU0:router(config)# rcc ipv6 unicast period 500
```
Or
```bash
RP/0/RP0/CPU0:router(config)# lcc ipv6 unicast enable
RP/0/RP0/CPU0:router(config)# lcc ipv6 unicast period 500
```

Triggers RCC or LCC background scan. Use the `period` option to control how often the verification is triggered. Each time the scan is triggered, verification is resumed from where it was left out, and one buffer’s worth of routes or labels are sent to the forwarding information base (FIB).

### Step 3: Use `commit` or `end` Command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts the user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session without committing the configuration changes.

### Step 4: View Scan Statistics

Use one of these commands:
- `show rcc {ipv4 | ipv6} unicast [summary | scan-id scan-id-value]`
- `show lcc {ipv4 | ipv6} unicast [summary | scan-id scan-id-value]`

**Example:**
```bash
RP/0/RP0/CPU0:router# show rcc ipv6 unicast statistics scan-id 120
```
Or
```bash
RP/0/RP0/CPU0:router# show lcc ipv6 unicast statistics scan-id 120
```

Displays statistics about background scans:
- `summary` — Displays the current ongoing scan ID and a summary of the previous few scans.
- `scan-id scan-id-value` — Displays details about a specific scan.

## Enabling RCC and LCC: Example

### Example 1: Enable RCC Background Scan for IPv6
```bash
rcc ipv6 unicast period 500
```
Enables Route Consistency Checker (RCC) background scan with a period of 500 milliseconds between buffers for IPv6 unicast tables.

### Example 2: Enable LCC Background Scan for IPv6
```bash
lcc ipv6 unicast period 500
```
Enables Label Consistency Checker (LCC) background scan with a period of 500 milliseconds between buffers for IPv6 unicast tables.

### Example 3: Run RCC On-Demand Scan for Subnet
```bash
show rcc ipv4 unicast 10.10.0.0/16 vrf vrf1
```
Runs Route Consistency Checker (RCC) on-demand scan for subnet `10.10.0.0/16` in `vrf1`.

### Example 4: Run LCC On-Demand Scan for All IPv6 Labels
```bash
show lcc ipv6 unicast all
```
Runs Label Consistency Checker (LCC) on-demand scan on all labels for IPv6 prefixes.
```
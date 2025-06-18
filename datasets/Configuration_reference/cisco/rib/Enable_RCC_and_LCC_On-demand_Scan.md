```markdown
# Enable RCC and LCC On-demand Scan

Perform this task to trigger route consistency checker (RCC) and Label Consistency Checker (LCC) on-demand scan. The on-demand scan can be run on a particular address family (AFI), sub address family (SAFI), table and prefix, vrf, or all prefixes in the table.

## SUMMARY STEPS

1. Use one of these commands:
   - `show rcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name]`
   - `show lcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name]`

2. Use one of these commands:
   - `clear rcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name] log`
   - `clear lcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name] log`

## DETAILED STEPS

### Step 1

Use one of these commands:
- `show rcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name]`
- `show lcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name]`

Example:

```bash
RP/0/RP0/CPU0:router#show rcc ipv6 unicast 2001:DB8::/32 vrf vrf_1
```

Or

```bash
RP/0/RP0/CPU0:router#show lcc ipv6 unicast 2001:DB8::/32 vrf vrf_1
```

Runs on-demand Route Consistency Checker (RCC) or Label Consistency Checker (LCC).

### Step 2

Use one of these commands:
- `clear rcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name] log`
- `clear lcc {ipv4 | ipv6} unicast [all] [prefix/mask] [vrf vrf-name] log`

Example:

```bash
RP/0/RP0/CPU0:router#clear rcc ipv6 unicast log
```

Or

```bash
RP/0/RP0/CPU0:router#show lcc ipv6 unicast log
```

Clears the log of previous scans.
```
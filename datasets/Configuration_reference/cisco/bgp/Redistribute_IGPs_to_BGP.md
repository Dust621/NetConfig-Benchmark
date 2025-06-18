```markdown
# Redistribute IGPs to BGP

Perform this task to configure redistribution of a protocol into the VRF address family.

Even if Interior Gateway Protocols (IGPs) are used as the PE-CE protocol, the import logic happens through BGP. Therefore, all IGP routes have to be imported into the BGP VRF table.

## SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `vrf vrf-name`
4. `address-family { ipv4 | ipv6 } unicast`
5. Do one of the following:

   - `redistribute connected [ metric metric-value ] [ route-policy route-policy-name ]`
   - `redistribute isis process-id [ level { 1 | 1-inter-area | 2 }] [ metric metric-value ] [ route-policy route-policy-name ]`
   - `redistribute ospf process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]`
   - `redistribute ospfv3 process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]`
   - `redistribute rip [ metric metric-value ] [ route-policy route-policy-name ]`
   - `redistribute static [ metric metric-value ] [ route-policy route-policy-name ]`

6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1: `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters configuration mode.

### Step 2: `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

### Step 3: `vrf vrf-name`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# vrf vrf_a
```

Enables BGP routing for a particular VRF on the PE router.

### Step 4: `address-family { ipv4 | ipv6 } unicast`

Example:

```bash
RP/0/RP0/CPU0:router(config-vrf)# address-family ipv4 unicast
```

Specifies either an IPv4 or IPv6 address family unicast and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

### Step 5: Redistribution Options

Do one of the following:

- `redistribute connected [ metric metric-value ] [ route-policy route-policy-name ]`
- `redistribute isis process-id [ level { 1 | 1-inter-area | 2 }] [ metric metric-value ] [ route-policy route-policy-name ]`
- `redistribute ospf process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]`
- `redistribute ospfv3 process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]`
- `redistribute rip [ metric metric-value ] [ route-policy route-policy-name ]`
- `redistribute static [ metric metric-value ] [ route-policy route-policy-name ]`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-vrf-af)# redistribute ospf 1
```

Configures redistribution of a protocol into the VRF address family context.

The `redistribute` command is used if BGP is not used between the PE-CE routers. If BGP is used between PE-CE routers, the IGP that is used has to be redistributed into BGP to establish VPN connectivity with other PE sites. Redistribution is also required for inter-table import and export.

### Step 6: Use the `commit` or `end` command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes**: Saves configuration changes and exits the configuration session.
  - **No**: Exits the configuration session without committing the configuration changes.
  - **Cancel**: Remains in the configuration session, without committing the configuration changes.
```
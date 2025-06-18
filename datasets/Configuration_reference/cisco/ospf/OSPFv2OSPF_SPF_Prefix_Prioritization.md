# OSPFv2 OSPF SPF Prefix Prioritization

The OSPFv2 OSPF SPF Prefix Prioritization feature enables an administrator to converge, in a faster mode, important prefixes during route installation.

When a large number of prefixes must be installed in the Routing Information Base (RIB) and the Forwarding Information Base (FIB), the update duration between the first and last prefix, during SPF, can be significant. In networks where time-sensitive traffic (for example, VoIP) may transit to the same router along with other traffic flows, it is important to prioritize RIB and FIB updates during SPF for these time-sensitive prefixes.

## Feature Overview

The OSPFv2 OSPF SPF Prefix Prioritization feature provides the administrator with the ability to prioritize important prefixes to be installed into the RIB during SPF calculations. Important prefixes converge faster among prefixes of the same route type per area. Before RIB and FIB installation, routes and prefixes are assigned to various priority batch queues in the OSPF local RIB, based on specified route policy. The RIB priority batch queues are classified as:

- **Critical**
- **High**
- **Medium**
- **Low**

When enabled, prefix alters the sequence of updating the RIB with this prefix priority:

```
Critical > High > Medium > Low
```

As soon as prefix priority is configured, `/32` prefixes are no longer preferred by default; they are placed in the low-priority queue, if they are not matched with higher-priority policies. Route policies must be devised to retain `/32s` in the higher-priority queues (high-priority or medium-priority queues).

Priority is specified using route policy, which can be matched based on IP addresses or route tags. During SPF, a prefix is checked against the specified route policy and is assigned to the appropriate RIB batch priority queue.

## Example Scenarios

- **If only high-priority route policy is specified, and no route policy is configured for a medium priority:**
  - Permitted prefixes are assigned to a high-priority queue.
  - Unmatched prefixes, including `/32s`, are placed in a low-priority queue.

- **If both high-priority and medium-priority route policies are specified, and no maps are specified for critical priority:**
  - Permitted prefixes matching high-priority route policy are assigned to a high-priority queue.
  - Permitted prefixes matching medium-priority route policy are placed in a medium-priority queue.
  - Unmatched prefixes, including `/32s`, are moved to a low-priority queue.

- **If both critical-priority and high-priority route policies are specified, and no maps are specified for medium priority:**
  - Permitted prefixes matching critical-priority route policy are assigned to a critical-priority queue.
  - Permitted prefixes matching high-priority route policy are assigned to a high-priority queue.
  - Unmatched prefixes, including `/32s`, are placed in a low-priority queue.

- **If only medium-priority route policy is specified and no maps are specified for high priority or critical priority:**
  - Permitted prefixes matching medium-priority route policy are assigned to a medium-priority queue.
  - Unmatched prefixes, including `/32s`, are placed in a low-priority queue.

## Configuration Commands

Use the following command to prioritize OSPFv2 OSPF prefix installation into the global RIB during SPF:

```bash
[no] spf prefix-priority route-policy rpl
```

SPF prefix prioritization is disabled by default. In disabled mode, `/32` prefixes are installed into the global RIB before other prefixes. If SPF prioritization is enabled, routes are matched against the route-policy criteria and are assigned to the appropriate priority queue based on the SPF priority set. Unmatched prefixes, including `/32s`, are placed in the low-priority queue.

If all `/32s` are desired in the high-priority queue or medium-priority queue, configure this single route map:

```bash
prefix-set ospf-medium-prefixes
  0.0.0.0/0 ge 32
end-set
```

## Configuration Steps

### Summary Steps

1. `configure`
2. `prefix-set prefix-set name`
3. `route-policy route-policy name`
   ```bash
   if destination in prefix-set name then set spf-priority {critical | high | medium} endif
   ```
4. Use one of these commands:
   - `router ospf ospf-name`
   - `router ospfv3 ospfv3-name`
5. `router ospf ospf name`
6. `spf prefix-priority route-policy route-policy name`
7. Use the `commit` or `end` command.
8. `show rpl route-policy route-policy name detail`

### Detailed Steps

#### Step 1: Enter Configuration Mode

```bash
RP/0/RP0/CPU0:router# configure
```

#### Step 2: Configure Prefix Set

```bash
RP/0/RP0/CPU0:router(config)# prefix-set ospf-critical-prefixes
RP/0/RP0/CPU0:router(config-pfx)# 66.0.0.0/16
RP/0/RP0/CPU0:router(config-pfx)# end-set
```

#### Step 3: Configure Route Policy

```bash
RP/0/RP0/CPU0:router# route-policy ospf-spf-priority
RP/0/RP0/CPU0:router(config-rpl)# if destination in ospf-critical-prefixes then set spf-priority critical endif
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```

#### Step 4: Enter Router OSPF Configuration Mode

```bash
RP/0/RP0/CPU0:router# router ospf 1
```
or
```bash
RP/0/RP0/CPU0:router# router ospfv3 1
```

#### Step 5: Configure SPF Prefix Priority

```bash
RP/0/RP0/CPU0:router(config-ospf)# spf prefix-priority route-policy ospf-spf-priority
```
or
```bash
RP/0/RP0/CPU0:router(config-ospfv3)# spf prefix-priority route-policy ospf3-spf-priority
```

#### Step 7: Commit or End Configuration

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

#### Step 8: Display SPF Prefix Priority

```bash
RP/0/RP0/CPU0:router# show rpl route-policy ospf-spf-priority detail
```

## Example Configuration

This example shows how to configure `/32` prefixes as medium-priority, in general, in addition to placing some `/32` and `/24` prefixes in critical-priority and high-priority queues:

```bash
prefix-set ospf-critical-prefixes
  192.41.5.41/32,
  11.1.3.0/24,
  192.168.0.44/32
end-set
!
prefix-set ospf-high-prefixes
  44.4.10.0/24,
  192.41.4.41/32,
  41.4.41.41/32
end-set
!
prefix-set ospf-medium-prefixes
  0.0.0.0/0 ge 32
end-set
!
route-policy ospf-priority
  if destination in ospf-high-prefixes then
    set spf-priority high
  else
    if destination in ospf-critical-prefixes then
      set spf-priority critical
    else
      if destination in ospf-medium-prefixes then
        set spf-priority medium
      endif
    endif
  endif
end-policy
!
router ospf 1
  spf prefix-priority route-policy ospf-priority
  area 0
    interface TenGigE 0/3/0/0
  !
  area 3
    interface TenGigE 0/2/0/0
  !
  area 8
    interface TenGigE 0/2/0/0
!
router ospfv3 1
  spf prefix-priority route-policy ospf-priority
  area 0
    interface TenGigE 0/3/0/0
  !
  area 3
    interface TenGigE 0/2/0/0
  !
  area 8
    interface TenGigE 0/2/0/0
```
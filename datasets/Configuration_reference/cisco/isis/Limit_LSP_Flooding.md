```markdown
# Limit LSP Flooding

Limiting link-state packets (LSP) may be desirable in certain "meshy" network topologies. An example of such a network might be a highly redundant one such as a fully meshed set of point-to-point links over a nonbroadcast multiaccess (NBMA) transport. In such networks, full LSP flooding can limit network scalability.

One way to restrict the size of the flooding domain is to introduce hierarchy by using multiple Level 1 areas and a Level 2 area. However, two other techniques can be used instead of or with hierarchy:

- Block flooding on specific interfaces
- Configure mesh groups

Both techniques operate by restricting the flooding of LSPs in some fashion. A direct consequence is that although scalability of the network is improved, the reliability of the network (in the face of failures) is reduced because a series of failures may prevent LSPs from being flooded throughout the network, even though links exist that would allow flooding if blocking or mesh groups had not restricted their use. In such a case, the link-state databases of different routers in the network may no longer be synchronized. Consequences such as persistent forwarding loops can ensue.

For this reason, we recommend that blocking or mesh groups be used only if specifically required, and then only after careful network design.

## Control LSP Flooding for IS-IS

Flooding of LSPs can limit network scalability. You can control LSP flooding by tuning your LSP database parameters on the router globally or on the interface. This task is optional.

Many of the commands to control LSP flooding contain an option to specify the level to which they apply. Without the option, the command applies to both levels. If an option is configured for one level, the other level continues to use the default value. To configure options for both levels, use the command twice. For example:

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-refresh-interval 1200 level 2
RP/0/RP0/CPU0:router(config-isis)# lsp-refresh-interval 1100 level 1
```

## SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `lsp-refresh-interval seconds [ level { 1 | 2 }]`
4. `lsp-check-interval seconds [ level { 1 | 2 }]`
5. `lsp-gen-interval { [ initial-wait initial | secondary-wait secondary | maximum-wait maximum ] ... } [ level { 1 | 2 }]`
6. `lsp-mtu bytes [ level { 1 | 2 }]`
7. `max-lsp-lifetime seconds [ level { 1 | 2 }]`
8. `ignore-lsp-errors disable`
9. `interface type interface-path-id`
10. `lsp-interval milliseconds [ level { 1 | 2 }]`
11. `csnp-interval seconds [ level { 1 | 2 }]`
12. `retransmit-interval seconds [ level { 1 | 2 }]`
13. `retransmit-throttle-interval milliseconds [ level { 1 | 2 }]`
14. `mesh-group { number | blocked }`
15. Use the `commit` or `end` command.
16. `show isis interface [ type interface-path-id | level { 1 | 2 }] [ brief ]`
17. `show isis [ instance instance-id ] database [ level { 1 | 2 }] [ detail | summary | verbose ] [ * | lsp-id ]`
18. `show isis [ instance instance-id ] lsp-log [ level { 1 | 2 }]`
19. `show isis database-log [ level { 1 | 2 }]`

## DETAILED STEPS

### Step 1: `configure`

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

### Step 2: `router isis instance-id`

```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```

Enables IS-IS routing for the specified routing instance, and places the router in router configuration mode.

- You can change the level of routing to be performed by a particular routing instance by using the `is-type` router configuration command.

### Step 3: `lsp-refresh-interval seconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-refresh-interval 10800
```

(Optional) Sets the time between regeneration of LSPs that contain different sequence numbers.

- The refresh interval should always be set lower than the `max-lsp-lifetime` command.

### Step 4: `lsp-check-interval seconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-check-interval 240
```

(Optional) Configures the time between periodic checks of the entire database to validate the checksums of the LSPs in the database.

- This operation is costly in terms of CPU and so should be configured to occur infrequently.

### Step 5: `lsp-gen-interval { [ initial-wait initial | secondary-wait secondary | maximum-wait maximum ] ... } [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-gen-interval maximum-wait 15 initial-wait 5 secondary-wait 5
```

(Optional) Reduces the rate of LSP generation during periods of instability in the network. Helps reduce the CPU load on the router and number of LSP transmissions to its IS-IS neighbors.

- During prolonged periods of network instability, repeated recalculation of LSPs can cause an increased CPU load on the local router. Further, the flooding of these recalculated LSPs to the other Intermediate Systems in the network causes increased traffic and can result in other routers having to spend more time running route calculations.

### Step 6: `lsp-mtu bytes [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-mtu 1300
```

(Optional) Sets the maximum transmission unit (MTU) size of LSPs.

### Step 7: `max-lsp-lifetime seconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis)# max-lsp-lifetime 11000
```

(Optional) Sets the initial lifetime given to an LSP originated by the router.

- This is the amount of time that the LSP persists in the database of a neighbor unless the LSP is regenerated or refreshed.

### Step 8: `ignore-lsp-errors disable`

```bash
RP/0/RP0/CPU0:router(config-isis)# ignore-lsp-errors disable
```

(Optional) Sets the router to purge LSPs received with checksum errors.

### Step 9: `interface type interface-path-id`

```bash
RP/0/RP0/CPU0:router(config-isis)# interface HundredGigE 0/1/0/3
```

Enters interface configuration mode.

### Step 10: `lsp-interval milliseconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis-if)# lsp-interval 100
```

(Optional) Configures the amount of time between each LSP sent on an interface.

### Step 11: `csnp-interval seconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis-if)# csnp-interval 30 level 1
```

(Optional) Configures the interval at which periodic CSNP packets are sent on broadcast interfaces.

- Sending more frequent CSNPs means that adjacent routers must work harder to receive them.
- Sending less frequent CSNP means that differences in the adjacent routers may persist longer.

### Step 12: `retransmit-interval seconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis-if)# retransmit-interval 60
```

(Optional) Configures the amount of time that the sending router waits for an acknowledgment before it considers that the LSP was not received and subsequently resends.

### Step 13: `retransmit-throttle-interval milliseconds [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router(config-isis-if)# retransmit-throttle-interval 1000
```

(Optional) Configures the amount of time between retransmissions on each LSP on a point-to-point interface.

- This time is usually greater than or equal to the `lsp-interval` command time because the reason for lost LSPs may be that a neighboring router is busy. A longer interval gives the neighbor more time to receive transmissions.

### Step 14: `mesh-group { number | blocked }`

```bash
RP/0/RP0/CPU0:router(config-isis-if)# mesh-group blocked
```

(Optional) Optimizes LSP flooding in NBMA networks with highly meshed, point-to-point topologies.

- This command is appropriate only for an NBMA network with highly meshed, point-to-point topologies.

### Step 15: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` — Exits the configuration session without committing the configuration changes.
  - `Cancel` — Remains in the configuration session, without committing the configuration changes.

### Step 16: `show isis interface [ type interface-path-id | level { 1 | 2 }] [ brief ]`

```bash
RP/0/RP0/CPU0:router# show isis interface HundredGigE 0/1/0/1 brief
```

(Optional) Displays information about the IS-IS interface.

### Step 17: `show isis [ instance instance-id ] database [ level { 1 | 2 }] [ detail | summary | verbose ] [ * | lsp-id ]`

```bash
RP/0/RP0/CPU0:router# show isis database level 1
```

(Optional) Displays the IS-IS LSP database.

### Step 18: `show isis [ instance instance-id ] lsp-log [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router# show isis lsp-log
```

(Optional) Displays LSP log information.

### Step 19: `show isis database-log [ level { 1 | 2 }]`

```bash
RP/0/RP0/CPU0:router# show isis database-log level 1
```

(Optional) Display IS-IS database log information.
```